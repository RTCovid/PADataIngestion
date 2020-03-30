#!/usr/bin/env python3
import pysftp
from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection
import tempfile
import shutil
import os
import csv
import base64

# TODO: Log all of this
# track success
# move to classes 


def load_credentials():
    creds = {}
    with open("creds.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            creds[row['service']] = {}
            creds[row['service']]['username'] = row['username']
            creds[row['service']]['password'] = row['password']
            creds[row['service']]['host'] = row['host']

    return creds
        

# On Google Cloud, only /tmp is writeable.
def get_latest_file(creds, prefix="HOS_ResourceCapacity", target_dir="/tmp/"):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys.load('copaftp.pub')
    username = creds['sftp']['username']
    password = creds['sftp']['password']
    host = creds['sftp']['host']
    with pysftp.Connection(host, username=username, password=password, cnopts=cnopts) as sftp:
        files = sftp.listdir()
        files = [f for f in files if f.startswith("HOS_ResourceCapacity")]
        # the files are sorted by the pysftp library, and the last element of the list is the latest file
        # Filenames look like HOS_ResourceCapacity_2020-03-30_00-00.csv
        # And timestamps are in UTC
        latest_filename = files[-1]
        print("The latest file is: f{latest_filename}")
        sftp.get(latest_filename, f'{target_dir}/{latest_filename}')
        print("Finished downloading f{latest_filename}")
        return (latest_filename, target_dir)

def upload_to_arcgis(creds, source_data_dir, source_data_file, original_data_file_name, 
                    arcgis_item_id_for_feature_layer):
    username = creds['arcgis']['username']
    password = creds['arcgis']['password']
    host = creds['arcgis']['host']

    gis = GIS(host, username, password) 

    # You might ask - why do you not just use the FeatureLayerCollection's URL?
    # Because you get a 403 if you try that. Instead, if you grab the parent container
    # from the published layer, you can use the FLC manager's overwrite() method successfully.

    feature_item = gis.content.get(arcgis_item_id_for_feature_layer)
    fs = feature_item.layers[0].container

    # Overwrite docs:
    # https://developers.arcgis.com/python/api-reference/arcgis.features.managers.html#featurelayercollectionmanager

    # Note that the filename (not the path, just the filename) must match the filename of the data the feature layer
    # was originally created from, because reasons. We rename here.

    # Note that if you have a feature service you want to use overwrite() on, you must share that
    # feature service with everyone (share->everyone). If you don't, you'll get a 403. You must also
    # share the underlying CSV with everyone.
    result = ""


    with tempfile.TemporaryDirectory() as tmpdirname:
        shutil.copyfile(os.path.join(source_data_dir, source_data_file), 
                        os.path.join(tmpdirname, original_data_file_name))

        original_dir = os.getcwd()
        os.chdir(tmpdirname)
        result = fs.manager.overwrite(original_data_file_name)
        os.chdir(original_dir)
        os.remove(os.path.join(source_data_dir, source_data_file))
    return result


def main():
    # The name of the file you created the layer service with.
    original_data_file_name = "HOS_ResourceCapacity_2020-03-28_21-00.csv"
    # You can get this id from the URL in arcgis online when you look at layer; eg:
    # https://pema.maps.arcgis.com/home/item.html?id=b815071a19394023872f5dd88f273614
    arcgis_item_id_for_feature_layer = "b815071a19394023872f5dd88f273614"

    creds = load_credentials()
    latest_filename, data_dir= get_latest_file(creds)
    print(data_dir, latest_filename)
    status = upload_to_arcgis(creds, data_dir, latest_filename, 
                            original_data_file_name, arcgis_item_id_for_feature_layer)
    print(latest_filename, status)


def hello_pubsub(event, context):
    main()

if __name__== "__main__":
    main()
