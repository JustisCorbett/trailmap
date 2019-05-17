import folium
import json
import os
#from app import db
from models import Trail, Comment, User
from sqlalchemy.orm import joinedload



def mapperfunc():
    """create a new folium map with geojson markers"""

    # load geojson data into a dict
    file = os.path.join('static', 'trailheadsjson.geojson')
    with open(file) as data:
        geo = json.load(data)

    
    # load trails and comments from database
    query = Trail.query.options(joinedload('comments'))
    #for trail in query:
        #print(trail, trail.comments)

    # create map object
    m = folium.Map(
        location=[39.804298, -111.415337],
        zoom_start=7,
        attr='© <a href="www.openstreetmap.org">OpenStreetMap<a> contributors',
        width='100%',
        height='90%'
    )
    tooltip = 'Click for More Info'

    # create markers from geojson dict
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
        popup = popuper(name, query)
        folium.Marker(
            list(reversed(coordinates)),
            popup="name",
            tooltip=tooltip,
            icon=folium.Icon(color=custom_color, icon=custom_icon, prefix='fa')
        ).add_to(m)

    # save map
    file_save = os.path.join('templates', 'map.html')
    m.save(file_save)


def popuper(name, query):
    """create popup for folium marker from database data"""
    #trail = query.trailname(name)
    print(query)
    #popup = folium.Popup(htlm=True, )
    return name


if __name__ == '__main__':
    mapperfunc()
