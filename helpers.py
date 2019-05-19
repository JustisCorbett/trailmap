import folium
import json
import os
from flask import Markup
from app import db
from models import Trail, Comment, User
from sqlalchemy.orm import joinedload
from folium.plugins import MarkerCluster
from sqlalchemy import func



def mapperfunc():
    """create a new folium map with geojson markers"""

    # load geojson data into a dict
    file = os.path.join('static', 'trailheadsjson.geojson')
    with open(file) as data:
        geo = json.load(data)

    # load trails and comment ratings from database if the trail has ratings
    query = (
            db.session.query(Trail.trailname, func.avg(Comment.rate_good),
                             func.avg(Comment.rate_hard))
            .join(Comment, Trail.comments)
            .group_by(Trail.trailname)
    )
    print(query)
    for trailname, rate_good, rate_hard in query:
        print(trailname, round(rate_good), round(rate_hard))

    # create map object
    m = folium.Map(
        location=[39.804298, -111.415337],
        zoom_start=7,
        attr='© <a href="www.openstreetmap.org">OpenStreetMap contributors<a> <a href="https://gis.utah.gov/">Utah AGRC</a>',
        width='100%',
        height='90%'
    )
    tooltip = 'Click for More Info'
    mc = MarkerCluster()

    # create markers from geojson dict, add to marker cluster
    for features in geo['features']:
        if features['properties']['Comments'] == 'OVPrimaryUseMTB':
            custom_icon = 'fa-bicycle'
            custom_color = 'orange'
        elif features['properties']['Comments'] == 'OVPrimaryUseHIKE':
            custom_icon = 'fa-male'
            custom_color = 'green'
        else:
            custom_icon = 'fa-arrows'
            custom_color = 'blue'
        name = features['properties']['PrimaryName']
        coordinates = features['geometry']['coordinates']
        popup = folium.Popup(popuper(name, query))
        folium.Marker(
            list(reversed(coordinates)),
            popup="name",
            tooltip=tooltip,
            icon=folium.Icon(color=custom_color, icon=custom_icon, prefix='fa')
        ).add_to(mc)

    # add marker cluster to map
    mc.add_to(m)

    # save map
    file_save = os.path.join('templates', 'map.html')
    m.save(file_save)


def popuper(name, query):
    """create popup for folium marker from database data"""
    rating = {
        1: Markup('<div class="rating"><span class="fa fa-star"></span><span class="fa fa-star-o"></span><span class="fa fa-star-o"></span><span class="fa fa-star-o"></span><span class="fa fa-star-o"></span><p class ="rate-text">Average User Rating</p></div>')
        2: Markup('<div class="rating"><span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star-o"></span><span class="fa fa-star-o"></span><span class="fa fa-star-o"></span><p class ="rate-text">Average User Rating</p></div>')
        3: Markup('<div class="rating"><span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star-o"></span><span class="fa fa-star-o"></span><p class ="rate-text">Average User Rating</p></div>')
        4: Markup('<div class="rating"><span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star-o"></span><p class ="rate-text">Average User Rating</p></div>')
        5: markup('<div class="rating"><span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star"></span><span class="fa fa-star"></span><p class ="rate-text">Average User Rating</p></div>')
    }
    print(rating[1])
    for trailname, rate_good, rate_hard in query:
        if trailname == name:
            html = "<div>" + trailname + ""
            return html
    #trail = query.filter_by(trailname=name).first()
    #popup = folium.Popup(htlm=True, )
    return name


if __name__ == '__main__':
    MapConstuctor()
