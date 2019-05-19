from app import db
from models import User, Trail, Comment


#user = User(username='bob', email='bob@bob.com', pw_hash='sdfdf')
post = Comment(user_id=1, trail_id=232, rate_good=4, rate_hard=5, post="okay")
db.session.add(post)
db.session.commit()
db.create_all()