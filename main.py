#!/usr/bin/env python3
import pysftp
from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection, FeatureSet, Table, Feature
import tempfile
import shutil
import os
import csv
import base64
import pandas as pd
import header_mapping as hm
from datetime import datetime
from pprint import pprint
import glob
import argparse
from geo_utils import HospitalLocations, Counties
from operators.process_csv import process_csv



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
def get_files_from_sftp(creds, prefix="HOS_ResourceCapacity_", target_dir="/tmp", 
                               only_latest=True, filenames_to_ignore=[]):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys.load('copaftp.pub')
    username = creds['sftp']['username']
    password = creds['sftp']['password']
    host = creds['sftp']['host']
    latest_filename = ""
    files = ""
    file_details = []

    existing_files = glob.glob(target_dir + "/" + prefix + "*")

    with pysftp.Connection(host, username=username, password=password, cnopts=cnopts) as sftp:
        files = sftp.listdir()
        files = [f for f in files if f.startswith(prefix)]
        # the files are sorted by the pysftp library, and the last element of the list is the latest file
        # Filenames look like HOS_ResourceCapacity_2020-03-30_00-00.csv
        # And timestamps are in UTC
        files_to_get = []
        if only_latest:
            latest_filename = files[-1]
            files_to_get = [latest_filename]
        else:
            files_to_get = files
        for f in files_to_get:
            if f in filenames_to_ignore:
                print(f"Ignoring {f}")
                continue
            print(f"Getting: {f}")
            if os.path.join(target_dir, f) not in existing_files:
                sftp.get(f, f'{target_dir}/{f}')
                print(f"Finished downloading {target_dir}/{f}")
            else:
                print(f"Didn't have to download {target_dir}/{f}; it already exists")

            source_date = f.split('.')[0]
            source_date = source_date.replace(prefix,'')
            source_date = source_date + " UTC"
            source_date = datetime.strptime(source_date, "%Y-%m-%d_%H-%M %Z")
            file_details.append({"dir": target_dir, "filename": f, "source_datetime": source_date})
    return (file_details, files)


def get_gis(creds):
    username = creds['arcgis']['username']
    password = creds['arcgis']['password']
    host = creds['arcgis']['host']

    gis = GIS(host, username, password) 
    return gis

def get_arcgis_feature_collection_from_item_id(gis, arcgis_item_id):

    # You might ask - why do you not just use the FeatureLayerCollection's URL?
    # Because you get a 403 if you try that. Instead, if you grab the parent container
    # from the published layer, you can use the FLC manager's overwrite() method successfully.

    feature_item = gis.content.get(arcgis_item_id)
    if "type:Table" in str(feature_item):
        fs = feature_item.tables[0].container
    else:
        fs = feature_item.layers[0].container
    return fs

def upload_to_arcgis(gis, source_data_dir, source_data_file, original_data_file_name, 
                    arcgis_item_id_for_feature_layer):

    fs = get_arcgis_feature_collection_from_item_id(gis, arcgis_item_id_for_feature_layer)
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
        print(f"Uploading to ArcGIS: {source_data_dir}/{source_data_file} as {original_data_file_name} to item id {arcgis_item_id_for_feature_layer}")
        try:
            result = fs.manager.overwrite(original_data_file_name)
        except Exception as e:
            print(f"Caught exception {e}, retrying")
            result = fs.manager.overwrite(original_data_file_name)

        os.chdir(original_dir)
        #os.remove(os.path.join(source_data_dir, source_data_file))
    return result

def load_csv_to_df(csv_file_path):
    df = pd.read_csv(csv_file_path)
    return df

def create_supplies_table(df):
    columns = ["Type"]
    for s, col_name in hm.supplies_on_hand_headers.items():
        columns.append(col_name)

    new_df = pd.DataFrame(columns=columns)

    for supply_type, value in hm.columns_to_sum_for_supplies_on_hand.items():
        new_row = {}
        new_row["Type"] = supply_type
        for time_window, column_name in value.items():
            new_row[hm.supplies_on_hand_headers[time_window]] = df[column_name].count()
        new_df = new_df.append(new_row, ignore_index=True)

    return new_df



def create_summary_table_row(df, source_data_timestamp, source_filename):
    new_row = {}
    new_row["Source Data Timestamp"] = source_data_timestamp.isoformat()
    new_row["Processed At"] = datetime.utcnow().isoformat()
    new_row["Source Filename"] = source_filename

    for pct_col_name, value in hm.summary_table_header.items():
        pct = (df[value["n"]].sum() / df[value["d"]].sum()) * 100

        new_row[value["d"]] = df[value["d"]].sum()
        new_row[value["n"]] = df[value["n"]].sum()
        new_row[pct_col_name] = pct
    return new_row

def process_hospital(gis, processed_dir, processed_filename, arcgis_item_id, original_data_file_name, dry_run=False):
    print("Starting load of hospital data")
    if dry_run:
        print("Dry run set, not uploading HOS table to ArcGIS.")
        status = "Dry run"
    else:
        status = upload_to_arcgis(gis, processed_dir, processed_filename, 
                            original_data_file_name, arcgis_item_id)
    print(status)
    print("Finished load of hospital data")
    return processed_dir, processed_filename

def process_supplies(gis, processed_dir, processed_filename, dry_run=False):
    print("Starting load of supplies data")
    original_data_file_name = "supplies.csv"
    arcgis_supplies_item_id = "8fad710d5df6434f8567373979dd9dbe"
    supplies_filename = "supplies.csv"

    df = load_csv_to_df(os.path.join(processed_dir, processed_filename))
    supplies = create_supplies_table(df)

    supplies.to_csv(os.path.join(processed_dir, supplies_filename), index=False)

    if dry_run:
        print("Dry run set, not uploading summary table to ArcGIS.")
        status = "Dry run"
    else:
        status = upload_to_arcgis(gis, processed_dir, supplies_filename, 
                            original_data_file_name, arcgis_supplies_item_id)
    print(status)
    print("Finished load of supplies data")


def get_files_to_not_sftp(gis, item_id):
    fs = gis.content.get(item_id)

    if "type:Table" in str(fs):
        t = fs.tables[0]
    else:
        t = fs.layers[0]

    qr = t.query(out_fields='Source_Filename')
    filenames_to_not_sftp = []
    for f in qr.features:
        filenames_to_not_sftp.append(f.attributes['Source_Filename'])
    filenames_to_not_sftp = list(set(filenames_to_not_sftp))
    return filenames_to_not_sftp

def process_historical_hos(gis, processed_dir, processed_file_details, dry_run=False):
    print("Starting load of historical HOS table...")
    original_data_file_name = "historical_hos_table.csv"
    arcgis_historical_item_id = "46f25552405a4fef9a6658fb5c0c68bf"


    table = gis.content.get(arcgis_historical_item_id)
    t = table.layers[0]

    new_col_names = {}
    for name in t.properties.fields:
        new_col_names[name["alias"]]  = name["name"]

    header = {}
    features = []
    for f in processed_file_details:
        fname = f["processed_filename"]
        size = os.path.getsize(os.path.join(processed_dir, fname))
        if size > 0:
            processed_time =  datetime.utcnow().isoformat()
            with open(os.path.join(processed_dir, fname), newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # add our rows
                    new_row ={}
                    row["Source Data Timestamp"] = f["source_datetime"].isoformat()
                    row["Processed At"] = processed_time
                    row["Source Filename"] = f["filename"]
                    header.update(row)
                    # rename the headers based on alias
                    for alias, name in new_col_names.items():
                        if alias in row:
                            new_row[name] = row[alias]
                    ft = Feature(attributes=new_row)
                    features.append(ft)
        else:
            print(f"{fname} has a filesize of {size}, not processing.")

    # historical for generating a new source CSV
    # you'll need to create a new_rows list above
    #if len(new_rows) > 0:
    #    with open(original_data_file_name, "w") as csvfile:
    #        writer = csv.DictWriter(csvfile, fieldnames=header)
    #        writer.writeheader()
    #        writer.writerows(new_rows)
    # Done CSV generation

    # It's okay if features is empty; status will reflect arcgis telling us that,
    # but it won't stop the processing.
    fs = FeatureSet(features)
    if dry_run:
        print("Dry run set, not editing features.")
        status = "Dry run"
    else:
        status = t.edit_features(adds=features)
    print(status)
    print("Finished load of historical HOS table")

def process_county_summaries(gis, processed_dir, processed_filename, arcgis_item_id, dry_run=False):
    print("Starting load of county summary table...")
    original_data_file_name = "county_summary_table.csv"
    new_data_filename = "new_county_summary_table.csv"

    df = load_csv_to_df(os.path.join(processed_dir, processed_filename))
    d2 = df.groupby(["HospitalCounty"])[hm.county_sum_columns].sum().reset_index()
    
    # PA wants to see 0.0 for any county that doesn't have a hospital, so:
    existing_counties = set(d2["HospitalCounty"].to_list())
    c = Counties()
    all_counties = c.counties
    unused_counties = list(set(all_counties).difference(existing_counties))
    a_row = [0.0] * 9
    rows = []
    for county in unused_counties:
        rows.append([county] + a_row)
    row_df = pd.DataFrame(rows, columns=d2.columns)
    d2 = d2.append(row_df)

    d2.to_csv(os.path.join(processed_dir, new_data_filename), header=True, index=False)

    if dry_run:
        print("Dry run set, not uploading county summary table to ArcGIS.")
        status = "Dry run"
    else:
        status = upload_to_arcgis(gis, processed_dir, new_data_filename, 
                            original_data_file_name, arcgis_item_id)
    print(status)
    print("Finished load of county summary data")


def process_summaries(gis, processed_dir, processed_file_details, dry_run=False):
    print("Starting load of summary table...")
    original_data_file_name = "summary_table.csv"
    arcgis_summary_item_id = "ab2820906d2c4b7fa68fcf47a5261916"

    table = gis.content.get(arcgis_summary_item_id)
    t = table.tables[0]

    summary_df = pd.DataFrame()
    for f in processed_file_details:
        fname = f["processed_filename"]
        size = os.path.getsize(os.path.join(processed_dir, fname))
        if size > 0:
            df = load_csv_to_df(os.path.join(processed_dir, fname))
            table_row = create_summary_table_row(df,f["source_datetime"], f["filename"])
            summary_df = summary_df.append(table_row, ignore_index = True)
        else:
            print(f"{fname} has a filesize of {size}, not processing.")

    new_col_names = {}
    for name in t.properties.fields:
        new_col_names[name["alias"]]  = name["name"]
    summary_df = summary_df.rename(columns=new_col_names)
    df_as_dict = summary_df.to_dict(orient='records')

    features = []
    for r in df_as_dict:
        ft = Feature(attributes=r)
        features.append(ft)
    # It's okay if features is empty; status will reflect arcgis telling us that,
    # but it won't stop the processing.
    fs = FeatureSet(features)
    if dry_run:
        print("Dry run set, not editing features.")
        status = "Dry run"
    else:
        status = t.edit_features(adds=features)
    print(status)
    print("Finished load of summary table")


def process_instantaneous(creds, gis, dry_run=False):
    print("Processing instantaneous tables...")
    print("Getting latest HOS file from SFTP...")
    file_details, all_filenames = get_files_from_sftp(creds)
    data_dir = file_details[0]["dir"]
    latest_filename = file_details[0]["filename"]
    source_datetime = file_details[0]["source_datetime"]
    print("Finished.")

    # Public-only data
    public_processed_file_details = process_csv([file_details[0]],
                    output_prefix="public_processed_HOS_", columns_wanted=hm.columns_for_public_release)
    public_processed_filename = public_processed_file_details[0]["processed_filename"]
    public_processed_dir = public_processed_file_details[0]["output_dir"]

    # Full data
    processed_file_details = process_csv([file_details[0]])
    processed_filename = processed_file_details[0]["processed_filename"]
    processed_dir = processed_file_details[0]["output_dir"]

    print(f"Finished processing {data_dir}/{latest_filename}, file is {processed_dir}/{processed_filename}")
    # The name of the file you created the layer service with.
    original_data_file_name = "processed_HOS.csv"
    # The ArcGIS item id of the feature service
    # You can get this id from the URL in arcgis online when you look at layer; eg:
    # https://pema.maps.arcgis.com/home/item.html?id=b815071a19394023872f5dd88f273614
    # This would be the page with Source: Feature Service on it.
    arcgis_item_id_for_feature_layer = "38592574c8de4a02b180d6f65918e385"

    process_hospital(gis, processed_dir, processed_filename, arcgis_item_id_for_feature_layer, 
            original_data_file_name, dry_run=dry_run)

    # id for the public layer
    arcgis_item_id_for_public_feature_layer = "1affcef28be04f4f994c99dea72d1a0e"
    public_original_filename = "public_processed_HOS.csv"

    process_hospital(gis, public_processed_dir, public_processed_filename, 
         arcgis_item_id_for_public_feature_layer, public_original_filename, dry_run=dry_run)

    process_supplies(gis, processed_dir, processed_filename, dry_run=dry_run)


    # original that started failing:
    # arcgis_item_id_for_county_summaries = "98469d4595a54faab84e73f5f6a473ea"
    arcgis_item_id_for_county_summaries = "c9f90ca7c83e40b8b6f4106dd3b0dfed"
    process_county_summaries(gis, processed_dir, processed_filename, arcgis_item_id_for_county_summaries, dry_run=dry_run)
    print("Finished processing instantaneous tables.")

def process_historical(creds, gis, dry_run=False):
    print("Processing historical tables...")
    # These processors manage their own SFTP's, since they may need to get many files.

    # Summary table
    item_id = "ab2820906d2c4b7fa68fcf47a5261916"
    files_to_not_sftp = get_files_to_not_sftp(gis, item_id)
    file_details, all_filenames = get_files_from_sftp(creds, only_latest=False, filenames_to_ignore=files_to_not_sftp)

    if len(file_details) == 0:
        print("No new files to process for historical summary table data.")
    else:
        processed_file_details = process_csv(file_details)
        processed_dir = processed_file_details[0]["output_dir"]
        process_summaries(gis, processed_dir, processed_file_details, dry_run=dry_run)

    # Full HOS historical table
    item_id = "46f25552405a4fef9a6658fb5c0c68bf"
    files_to_not_sftp = []
    file_details = []
    all_filenames = []
    files_to_not_sftp = get_files_to_not_sftp(gis, item_id)
    file_details, all_filenames = get_files_from_sftp(creds, only_latest=False, filenames_to_ignore=files_to_not_sftp)
    if len(file_details) == 0:
        print("No new files to process for historical data.")
    else:
        processed_file_details = process_csv(file_details)
        processed_dir = processed_file_details[0]["output_dir"]
        process_historical_hos(gis, processed_dir, processed_file_details, dry_run=dry_run)

    print("Finished processing historical tables.")

def main(dry_run=False):
    print("Started ingestion processing run")
    creds = load_credentials()
    print("Connecting to ArcGIS...")
    gis = get_gis(creds)
    print("Connected.")
    process_instantaneous(creds, gis, dry_run=dry_run)
    process_historical(creds, gis, dry_run=dry_run)
    print("Finished ingestion processing run")

def hello_pubsub(event, context):
    main()

if __name__== "__main__":
    dry_run = False
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry_run")
    args = parser.parse_args()
    if args.dry_run is not None:
        dry_run = True
    main(dry_run)
