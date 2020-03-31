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
def get_latest_file(creds, prefix="HOS_ResourceCapacity", target_dir="/tmp"):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys.load('copaftp.pub')
    username = creds['sftp']['username']
    password = creds['sftp']['password']
    host = creds['sftp']['host']
    latest_filename = ""
    with pysftp.Connection(host, username=username, password=password, cnopts=cnopts) as sftp:
        files = sftp.listdir()
        files = [f for f in files if f.startswith("HOS_ResourceCapacity")]
        # the files are sorted by the pysftp library, and the last element of the list is the latest file
        # Filenames look like HOS_ResourceCapacity_2020-03-30_00-00.csv
        # And timestamps are in UTC
        latest_filename = files[-1]
        print(f"The latest file is: {latest_filename}")
        sftp.get(latest_filename, f'{target_dir}/{latest_filename}')
        print(f"Finished downloading {target_dir}/{latest_filename}")
    return (target_dir, latest_filename)


def process_csv(source_data_dir, source_data_file, tmpdir="/tmp"):
   # data = pd.read_csv(os.path.join(source_data_dir, source_data_file), engine="python")
    output_filename = "processed_HOS.csv"
    output_dir = tmpdir
    output_path = os.path.join(output_dir, output_filename)
    rows = []
    with open (os.path.join(source_data_dir, source_data_file), newline='') as rf:
        reader = csv.reader(rf)
        header = True
        for row in reader:
            if header:
                header_row = []
                for c in row:
                    if "'" in c:
                        c = c.replace("'", "")
                    header_row.append(c)
                rows.append(header_row)
                header = False
            else:
                rows.append(row)
    with open (output_path, 'w', newline='') as wf:
        writer = csv.writer(wf)
        writer.writerows(rows)
    return (output_dir, output_filename)

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
        #os.remove(os.path.join(source_data_dir, source_data_file))
    return result


def main():
    print("Started ingestion processing run")
    # The name of the file you created the layer service with.
    original_data_file_name = "processed_HOS.csv"
    # You can get this id from the URL in arcgis online when you look at layer; eg:
    # https://pema.maps.arcgis.com/home/item.html?id=b815071a19394023872f5dd88f273614
    # This would be the page with Source: Feature Service on it.
    arcgis_item_id_for_feature_layer = "38592574c8de4a02b180d6f65918e385"

    creds = load_credentials()
    data_dir, latest_filename = get_latest_file(creds)
    processed_dir, processed_filename = process_csv(data_dir, latest_filename)
    print(f"Finished processing {data_dir}/{latest_filename}, file is {processed_dir}/{processed_filename}")
    status = upload_to_arcgis(creds, processed_dir, processed_filename, 
                            original_data_file_name, arcgis_item_id_for_feature_layer)
    print(status)
    print("Finished ingestion processing run")


def hello_pubsub(event, context):
    main()

if __name__== "__main__":
    main()
