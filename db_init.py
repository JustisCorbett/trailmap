from app import db
from models import Trail, User, Comment
import json
import os


# load geojson data into a dict
file = os.path.join('static', 'trailheadsjson.geojson')
with open(file) as data:
    geo = json.load(data)


# create objects for insertion into database
for feature in geo['features']:
    trail = Trail(trailname=feature['properties']['PrimaryName'],
                  use=feature['properties']['Comments'])
    db.session.add(trail)
    db.session.commit()
db.create_all()
