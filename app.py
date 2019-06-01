from flask import Flask, redirect, render_template, session, request, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/flasktrails'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jqewotptknoxrj:54ea7f064f3ea562961843cf894e446774889fece265324e8b4e6ab7e3278ab6@ec2-54-163-226-238.compute-1.amazonaws.com:5432/d3jtih4nl7s405'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from helpers import mapmaker, login_required, apology
from models import User, Trail, Comment


@app.route("/")
def index():
    """Create and render map"""

    return render_template("index.html")


@app.route("/map")
def showmap():
    """return map file for use in iFrame"""

    mapmaker()
    map_path = os.path.join('templates', 'map.html')
    return send_file(map_path)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        return "TODO"
    else:
        return render_template("register.html")


@app.route("/check", methods=["GET"])
def check():
    """Check if user is registerable"""

    return jsonify(False)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    if request.method == "POST":
        return "TODO"
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""


@app.route("/changepw", methods=["GET", "POST"])
#@login_required
def changepw():
    """Change user's password"""


@app.route("/search", methods=["GET"])
def trailsearch():
    """Let user search all trails"""

    if "search" in request.args:
        return render_template("search.html")
    else:
        return render_template("search.html")


@app.route("/trail", methods=["GET"])
def trailposts():
    """Show posts for specified trail"""

    #name = request.args.get["name"]
    #trail = Trail.query.filter_by(trailname=name).first()
    #if not trail:
    return apology('message', 400)
    #else:
        #return render_template("trail.html")

@app.route("/comment", methods=["GET", "POST"])
@login_required
def comment():
    """Let user comment and rate a trail"""


@app.route("/user", methods=["GET"])
def user():
    """Show specified user's history of posts"""
