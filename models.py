from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username


class Trail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    use = db.Column(db.String(20))
    comments = db.relationship('Comment', backref='trail', lazy=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'),
        nullable=False)
    trail_id = db.Column(db.Integer, db.ForeignKey('Trail.id'),
        nullable=False)
    rate_good = db.Column(db.Integer)
    rate_hard = db.Column(db.Integer)
    post = db.Column(db.Text)
    time = db.Column(db.DateTime)
