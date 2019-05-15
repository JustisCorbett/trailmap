from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    pw_hash = db.Column(db.String(120), nullable=False)
    comments = db.relationship('Comment', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Trail(db.Model):
    __tablename__ = 'trail'
    id = db.Column(db.Integer, primary_key=True)
    trailname = db.Column(db.String(120), index=True, unique=True)
    use = db.Column(db.String(20))
    comments = db.relationship('Comment', backref='trail', lazy=True)

    def __repr__(self):
        return '<Trail {}>'.format(self.trailname)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
    trail_id = db.Column(db.Integer, db.ForeignKey('trail.id'),
                         nullable=False)
    rate_good = db.Column(db.Integer)
    rate_hard = db.Column(db.Integer)
    post = db.Column(db.Text)
    time = db.Column(db.DateTime)

    def __repr__(self):
        return '<Comment {}>'.format(self.post)
