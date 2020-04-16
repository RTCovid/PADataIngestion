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
from datetime import datetime, date, timedelta
from pprint import pprint
import glob
import argparse
from geo_utils import HospitalLocations, Counties
from operators import process_csv, get_files_from_sftp, get_gis, get_arcgis_feature_collection_from_item_id, upload_to_arcgis, get_already_processed_files
from operators import get_datetime_from_filename


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


def process_historical_hos(gis, processed_dir, processed_file_details, arcgis_historical_item_id, 
                            original_data_file_name="historical_hos_table_v2.csv", dry_run=False):
    print("Starting load of historical HOS table...")
  #  original_data_file_name = "historical_hos_table.csv" # v1
  #  arcgis_historical_item_id = "46f25552405a4fef9a6658fb5c0c68bf" # v1

    table = gis.content.get(arcgis_historical_item_id)
    t = table.layers[0]

    new_col_names = {}
    for name in t.properties.fields:
        new_col_names[name["alias"]]  = name["name"]

    header = {}
    features = []
    new_rows = []
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
                    new_rows.append(row)
        else:
            print(f"{fname} has a filesize of {size}, not processing.")

    # historical for generating a new source CSV
#    if len(new_rows) > 0:
#        with open(os.path.join(processed_dir, original_data_file_name), "w") as csvfile:
#            writer = csv.DictWriter(csvfile, fieldnames=header)
#            writer.writeheader()
#            writer.writerows(new_rows)
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
    original_data_file_name = "county_summary_table_v3.csv"
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


def process_daily_hospital_averages(gis, historical_gis_item_id, daily_averages_item_id, dry_run=False):
    # see what days have been processed
    # if not processed, 
    # get the historical table
    # turn it into a df
    # per day, get the averages
    # for new: days

    print("XXX daily_hospital_averages stub, returning.")
    table = gis.content.get(historical_gis_item_id)
    t = table.layers[0]


    days = [date.fromisoformat('2020-04-14')]
    #for filename in sorted(historical_already_processed_files):
    #    d = get_datetime_from_filename(filename)
    #    days.append(d.date())
    dfs=[]
    for day in days:
        day_before=day - timedelta(days=1)
        day_after=day + timedelta(days=1)
        day_before = day_before.isoformat()
        day_after = day_after.isoformat()
        where=f"Source_Data_Timestamp >= '{day_before}' and Source_Data_Timestamp < '{day_after}'"
        df = t.query(where=where, as_df=True)
        # select the correct columns!
        by_hospital_df = df.groupby(["HospitalName"]).mean().reset_index()
        by_county_df = df.groupby(["HospitalCounty"]).mean().reset_index()
        # and upload them
#    print(df)

#    new_col_names = {}
#    for name in t.properties.fields:
#        new_col_names[name["name"]]  = name["alias"]
#
#    df = df.rename(columns=new_col_names)
#    print(df)
#
#    df.to_csv("/tmp/one_day.csv", index=False, header=True)
#    os.exit()

#    pass
    


def process_instantaneous(dry_run=False):
    print("Processing instantaneous tables...")
    creds = load_credentials()
    print("Connecting to ArcGIS...")
    gis = get_gis(creds)
    print("Connected.")
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
    # arcgis_item_id_for_county_summaries = "98469d4595a54faab84e73f5f6a473ea" #v1
    #arcgis_item_id_for_county_summaries = "c9f90ca7c83e40b8b6f4106dd3b0dfed" # v2
    arcgis_item_id_for_county_summaries = "a6b94769b5aa47e28790770826b55875" # v3
    process_county_summaries(gis, processed_dir, processed_filename, arcgis_item_id_for_county_summaries, dry_run=dry_run)
    print("Finished processing instantaneous tables.")

def process_historical(dry_run=False):
    print("Processing historical tables...")
    creds = load_credentials()
    print("Connecting to ArcGIS...")
    gis = get_gis(creds)
    print("Connected.")
    # These processors manage their own SFTP's, since they may need to get many files.

    # Summary table
    item_id = "ab2820906d2c4b7fa68fcf47a5261916"
    files_to_not_sftp = get_already_processed_files(gis, item_id)
    file_details, all_filenames = get_files_from_sftp(creds, only_latest=False, filenames_to_ignore=files_to_not_sftp)

    if len(file_details) == 0:
        print("No new files to process for historical summary table data.")
    else:
        processed_file_details = process_csv(file_details)
        processed_dir = processed_file_details[0]["output_dir"]
        process_summaries(gis, processed_dir, processed_file_details, dry_run=dry_run)

    # Full HOS historical table
    item_id = "46f25552405a4fef9a6658fb5c0c68bf"
    item_id = "bf24ecc40f294c1ba5ad16522f9be512" # v2
    files_to_not_sftp = []
    file_details = []
    all_filenames = []
    files_to_not_sftp = get_already_processed_files(gis, item_id)

    file_details, all_filenames = get_files_from_sftp(creds, only_latest=False, filenames_to_ignore=files_to_not_sftp)
    if len(file_details) == 0:
        print("No new files to process for historical data.")
    else:
        processed_file_details = process_csv(file_details)
        processed_dir = processed_file_details[0]["output_dir"]
        process_historical_hos(gis, processed_dir, processed_file_details, item_id, dry_run=dry_run)


    print("Finished processing historical tables.")

# When you are developing new features, or testing them, put them here first,
# then when you are sure of them, promote them to the right place.
def process_canary_features(dry_run=False):
    print("Processing canary features...")
    creds = load_credentials()
    print("Connecting to ArcGIS...")
    gis = get_gis(creds)
    print("Connected.")

    print("XXX not doing historical averages yet")
    historical_gis_item_id = "bf24ecc40f294c1ba5ad16522f9be512" 
    historical_averages_item_id = ""
    process_daily_hospital_averages(gis, historical_gis_item_id, historical_averages_item_id, dry_run=dry_run)
    print("Finished canary features.")

def main(dry_run=False, csv_to_process=None):
    print("Started full ingestion processing run")
    #process_canary_features(dry_run=dry_run)
    process_instantaneous(dry_run=dry_run)
    process_historical(dry_run=dry_run)
    print("Finished full ingestion processing run")

def hello_pubsub(event, context):
    main()

def instantaneous_pubsub(event, context):
    print("Started instantaneous ingestion processing run")
    process_instantaneous()
    print("Finished instantaneous ingestion processing run")

def historical_pubsub(event, context):
    print("Started historical ingestion processing run")
    process_historical()
    print("Finished historical ingestion processing run")

if __name__== "__main__":
    dry_run = False
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry_run")
    args = parser.parse_args()
    if args.dry_run is not None:
        dry_run = True
    main(dry_run)
