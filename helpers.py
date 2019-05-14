import folium
import json
import os






def mapperfunc():
    """create a new folium map with geojson markers"""

    # load geojson data into a dict
    with open('trailheadsjson.geojson') as data:
        geo = json.load(data)

    # create map object
    m = folium.Map(
        location=[39.804298, -111.415337],
        zoom_start=7
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
        popup = popuper(name)
        print((popup), '\n')
        folium.Marker(
            list(reversed(coordinates)),
            popup="name",
            tooltip=tooltip,
            icon=folium.Icon(color=custom_color, icon=custom_icon, prefix='fa')
        ).add_to(m)

    # save map
    m.save("index.html")

def popuper(name):
    """create popup for folium marker from database data"""
    
    return name


if __name__ == '__main__':
    mapperfunc()