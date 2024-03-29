from flask import Flask, redirect, render_template, session, request, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from urllib.parse import quote_plus
from flask_moment import Moment
import os
from configparser import RawConfigParser

app = Flask(__name__)
app.secret_key = os.urandom(24)

config = RawConfigParser()
config.read('/web/settings.ini')

username = "utrailsuser"
password = config.get('pgpassword','password')
database = "utrails"
#DATABASE_URL = os.environ['DATABASE_URL']
#if DATABASE_URL.startswith("postgres://"):
#    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@localhost:5432/{database}"
#app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
moment = Moment(app)

from helpers import mapmaker, login_required, apology
from models import User, Trail, Comment


@app.route("/")
def index():
    """render the default map"""

    # remove trail in session to make default map
    session["trail"] = None
    return render_template("index.html")


@app.route("/map")
def showmap():
    """return map file for use in iFrame"""

    # if there is a trail variable pass it to mapmaker
    try:
        if session["trail"] is not None:
            trailParam = session["trail"]
        else:
            trailParam = ""
    except:
        trailParam = ""
    mapmaker(trailParam)
    map_path = os.path.join('templates', 'map.html')
    return send_file(map_path)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session["user_id"] = None

    # Ensure user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check for form errors
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("email"):
            return apology("must provide email", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must be identical", 400)

        # hash password
        pw_hash = generate_password_hash(request.form.get("password"))

        # query db to see if they already exist
        result_name = User.query.filter_by(username=request.form.get("username")).first()
        result_email = User.query.filter_by(email=request.form.get("email")).first()

        # if username or email is already in db return apology, else insert into db
        if not result_name or not result_email:
            user = User(username=request.form.get("username"),
                        email=request.form.get("email"),
                        pw_hash=pw_hash)
            db.session.add(user)
            db.session.commit()
        else:
            return apology("Username and/or Email is already taken", 400)

        # log in user and redirect to home
        session["user_id"] = user.id

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/check", methods=["GET"])
def check():
    """Check if user is registerable"""

    # check if username has value
    if not request.args.get("username"):
        return jsonify(False)
    elif not request.args.get("email"):
        return jsonify(False)

    # search db for name
    username = request.args.get("username")
    email = request.args.get("email")
    result_name = User.query.filter_by(username=username).first()
    result_email = User.query.filter_by(email=email).first()

    # return true if available
    if not result_name and not result_email:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session["user_id"] = None

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username and password was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        result = User.query.filter_by(username=request.form.get("username")).first()

        # Ensure username exists and password is correct
        if not result or not check_password_hash(result.pw_hash, request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = result.id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session["user_id"] = None

    # Redirect user to login form
    return redirect("/login")


@app.route("/changepw", methods=["GET", "POST"])
@login_required
def changepw():
    """Change user's password"""

    if request.method == "POST":
        user_id = session["user_id"]
        old_pw = request.form.get("old-pw")
        new_pw = request.form.get("new-pw")

        update_user = User.query.filter(User.id == user_id).first()

        if not check_password_hash(update_user.pw_hash, old_pw):
            return apology("invalid old password", 400)
        else:
            update_user.pw_hash = generate_password_hash(new_pw)
            db.session.commit()
            return render_template("index.html")

    else:
        return render_template("changepw.html")


@app.route("/search", methods=["GET"])
def trailsearch():
    """Let user search for users and trails"""

    # get query string from args, search db and pass query objects to template
    query = request.args.get("search")
    looking_for = f"%{query}%"
    
    result_trails = Trail.query.filter(Trail.trailname.ilike(looking_for)).all()
    result_users = User.query.filter(User.username.ilike(looking_for)).all()

    for trail in result_trails:
        trail.link = quote_plus(trail.trailname)
    for user in result_users:
        user.link = quote_plus(user.username)

    return render_template("search.html", trails=result_trails, users=result_users)


@app.route("/trail", methods=["GET"])
def trailposts():
    """Show posts for specified trail"""

    # save trail in session for use in map generation
    name = request.args.get("name")
    session["trail"] = name
    avg_ratings = {}

    result_trail = (
        db.session.query(Trail)
        .filter(Trail.trailname == name)
        .first()
    )
    result_comments = (
        db.session.query(Comment, User.username)
        .join(User)
        .filter(Comment.trail_id == result_trail.id)
        .order_by(Comment.time.desc())
    )
    result_ratings = (
        db.session.query(Trail.trailname, func.avg(Comment.rate_good),
                         func.avg(Comment.rate_hard))
        .join(Comment, Trail.comments)
        .group_by(Trail.trailname)
        .filter(Trail.trailname == name)
        .first()
    )
    if result_ratings:
        avg_ratings["rate_good"] = round(result_ratings[1])
        avg_ratings["rate_hard"] = round(result_ratings[2])
    elif not result_ratings:
        avg_ratings["rate_good"] = "Unrated"
        avg_ratings["rate_hard"] = "Unrated"

    if not result_trail:
        return apology('Trail Not Found', 404)
    else:
        return render_template("trail.html", trail=result_trail,
                               avg_ratings=avg_ratings,
                               comments=result_comments)


@app.route("/comment", methods=["POST"])
@login_required
def comment():
    """Let user comment and rate a trail"""

    # validate form
    if not request.form.get("comment"):
        return apology('You must add a comment to rate trail.', 400)

    # get variables for db insertion
    user_id = session["user_id"]
    trail_name = session["trail"]
    comment = request.form.get("comment")
    rate_good = request.form.get("rate-good")
    rate_hard = request.form.get("rate-hard")

    # query db for trail to get id
    result_trail = (
        db.session.query(Trail.id)
        .filter(Trail.trailname == trail_name)
        .first()
    )

    if not result_trail:
        return apology('Trail Not Found', 404)
    else:
        trail_id = result_trail[0]

    # create Comment and insert into db
    post = Comment(user_id=user_id,
                   trail_id=trail_id,
                   rate_good=rate_good,
                   rate_hard=rate_hard,
                   post=comment)

    db.session.add(post)
    db.session.commit()

    return render_template("success.html", trail_name=trail_name)


@app.route("/user", methods=["GET"])
def user():
    """Show specified user's history of posts"""

    name = request.args.get("name")

    result_user = (
        db.session.query(User)
        .filter(User.username == name)
        .first()
    )

    result_comments = (
        db.session.query(Comment)
        .filter(Comment.user_id == result_user.id)
        .order_by(Comment.time.desc())
    )

    return render_template("user.html", comments=result_comments,
                           user=result_user)


def errorhandler(e):
    """Handle error"""

    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
