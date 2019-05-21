import folium
import json
import os
from flask import Markup
from app import db
from models import Trail, Comment, User
from sqlalchemy.orm import joinedload
from folium.plugins import MarkerCluster
from sqlalchemy import func
from urllib.parse import quote_plus



def mapmaker():
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
    trails = {}
    for trailname, rate_good, rate_hard in query:
        trails[trailname] = (round(rate_good), round(rate_hard))

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
        popup = folium.Popup(popuper(name, trails), parse_html=True)
        folium.Marker(
            list(reversed(coordinates)),
            popup=popup,
            tooltip=tooltip,
            icon=folium.Icon(color=custom_color, icon=custom_icon, prefix='fa')
        ).add_to(mc)

    # add marker cluster to map
    mc.add_to(m)

    # save map
    file_save = os.path.join('templates', 'map.html')
    m.save(file_save)


def popuper(name, trails):
    """create popup for folium marker from database data"""

    quote = quote_plus(name)
    if name in trails:
        html_name = f"<div><h3><a href=\"/trail?name={quote}\">{name}</a></h3></div>"
        html_rate = f"<div><p>Average User Rating: {trails[name][0]}/5</p></div>"
        html_diff = f"<div><p>Average User Difficulty: {trails[name][1]}/5</p></div>"
    else:
        html_name = f"<div><h3><a href=\"/trail?name={quote}\">{name}</a></h3></div>"
        html_rate = f"<div><p>Average User Rating: unrated/5</p></div>"
        html_diff = f"<div><p>Average User Difficulty: unrated/5</p></div>"

    popup = f"<html>{html_name}{html_rate}{html_diff}</html>"
    print(popup)
    return popup


if __name__ == '__main__':
    mapmaker()
