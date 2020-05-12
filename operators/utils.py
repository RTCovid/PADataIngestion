import json
from datetime import datetime


def get_datetime_from_filename(filename, prefix="HOS_ResourceCapacity_"):
    source_date = filename.split('.')[0]
    source_date = source_date.replace(prefix,'')
    source_date = source_date + " UTC"
    source_date = datetime.strptime(source_date, "%Y-%m-%d_%H-%M %Z")
    return source_date


def load_geojson(filename, idfield):

    with open(filename, "r") as f:
        geojson = json.loads(f.read())

    outdata = {}

    for feature in geojson['features']:
        name = feature['properties'].pop(idfield)
        outdata[name] = feature['properties']
        outdata[name]["long"] = feature['geometry']['coordinates'][0]
        outdata[name]["lat"] = feature['geometry']['coordinates'][1]

    return outdata
