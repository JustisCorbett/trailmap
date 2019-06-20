import folium
import json
import os
from app import db
from models import Trail, Comment
from folium.plugins import MarkerCluster
from sqlalchemy import func
from urllib.parse import quote_plus
from flask import redirect, render_template, request, session
from functools import wraps


def mapmaker(trailParam):
    """Create a new folium map with geojson markers.
       If called with a trailParam, center map to trail and auto open popup"""

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

    # if there is a trail parameter, save coords
    if trailParam:
        for features in geo['features']:
            if features['properties']['PrimaryName'] == trailParam:
                trailParamCoords = features['geometry']["coordinates"]
    
    # create map object
    if not trailParam:
        m = folium.Map(
            location=[39.804298, -111.415337],
            zoom_start=7,
            attr='© <a href="www.openstreetmap.org">OpenStreetMap contributors<a>, <a href="https://gis.utah.gov/">Utah AGRC</a>',
            width='100%',
            height='100%'
        )
        tooltip = 'Click for More Info'
        mc = MarkerCluster()
    else:
        m = folium.Map(
            location=list(reversed(trailParamCoords)),
            zoom_start=15,
            attr='© <a href="www.openstreetmap.org">OpenStreetMap contributors<a>, <a href="https://gis.utah.gov/">Utah AGRC</a>',
            width='100%',
            height='100%'
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
        popup = popuper(name, trails)
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
    safe_name = name.replace("`", "")
    if name in trails:
        html_name = f"<div><h3><a href=\"/trail?name={quote}\">{safe_name}</a></h3></div>"
        html_rate = f"<div><p style=\"white-space: nowrap\">Average User Rating: {trails[name][0]}/5</p></div>"
        html_diff = f"<div><p style=\"white-space: nowrap\">Average User Difficulty: {trails[name][1]}/5</p></div>"
    else:
        html_name = f"<div><h3><a href=\"/trail?name={quote}\">{safe_name}</a></h3></div>"
        html_rate = f"<div><p style=\"white-space: nowrap\">Average User Rating: unrated/5</p></div>"
        html_diff = f"<div><p style=\"white-space: nowrap\">Average User Difficulty: unrated/5</p></div>"

    popup = f"<html>{html_name}{html_rate}{html_diff}</html>"
    return popup


def login_required(f):
    """Decorate routes to require login."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def apology(message, code=400):
    """Render message as an apology to user."""

    return render_template("apology.html", top=code, bottom=message)


if __name__ == '__main__':
    mapmaker()
