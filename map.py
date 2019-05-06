import shapefile  # "pip install pyshp"
from json import dumps

# read shp files

reader = shapefile.Reader("Trailheads/Trailheads")
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    geom = sr.shape.__geo_interface__
    buffer.append(dict(type="Feature",
                       geometry=geom, properties=atr))

print(fields)
print(reader)
print(dir(atr))
print(dir(geom))
# write the GeoJSON file

geojson = open("geojson/trailheads.json", "w")
geojson.write(dumps({"type": "FeatureCollection", "features": buffer},
                    indent=2) + "\n")
geojson.close()
