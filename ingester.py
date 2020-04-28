import os
import csv
import glob
import math
import pysftp
import pandas as pd
from pprint import pprint
from datetime import datetime, date, timedelta

import header_mapping as hm
from geo_utils import Counties
from operators import process_csv
from operators import get_datetime_from_filename
from arcgis.features import FeatureLayerCollection, FeatureSet, Table, Feature


def load_csv_to_df(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path)
    except UnicodeDecodeError:
        df = pd.read_csv(csv_file_path, encoding='cp1252')
    return df


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]


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


class Ingester(object):

    def __init__(self, dry_run=False):

        creds = self._load_credentials()
        if creds is None:
            raise Exception("no sftp credentials supplied")

        self.creds = creds
        self.dry_run = dry_run
        self.gis = None
        self.available_files = []

    def _load_credentials(self):

        cred_path = "creds.csv"
        if not os.path.isfile(cred_path):
            return None

        creds = {}
        with open(cred_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['service'] == 'sftp':
                    creds['username'] = row['username']
                    creds['password'] = row['password']
                    creds['host'] = row['host']
        return creds

    def set_gis(self, gis_object):

        self.gis = gis_object

    def get_files_from_sftp(self, prefix="HOS_ResourceCapacity_", target_dir="/tmp",
                                   only_latest=True, filenames_to_ignore=[]):

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys.load('copaftp.pub')
        username = self.creds['username']
        password = self.creds['password']
        host = self.creds['host']
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

                source_date = get_datetime_from_filename(f, prefix=prefix)
                file_details.append({"dir": target_dir, "filename": f, "source_datetime": source_date})
        return (file_details, files)

    def process_hospital(self, processed_dir, processed_filename, public=True):

        # public vs. non-public means different ArcGIS online items
        if public is True:
            dataset_name = "public_hospital_layer"
        else:
            dataset_name = "hospital_layer"

        print(f"Starting load of hospital data: {dataset_name}")
        if self.dry_run:
            print("Dry run set, not uploading HOS table to ArcGIS.")
            status = "Dry run"
        else:
            status = self.gis.overwrite_arcgis_layer(dataset_name, processed_dir, processed_filename)

        print(status)
        print(f"Finished load of hospital data: {dataset_name}")
        return processed_dir, processed_filename

    def process_supplies(self, processed_dir, processed_filename):
        print("Starting load of supplies data")

        # set the new file name using the original file name in the layers conf
        supplies_filename = self.gis.layers['supplies']['original_file_name']

        df = load_csv_to_df(os.path.join(processed_dir, processed_filename))
        supplies = create_supplies_table(df)

        supplies.to_csv(os.path.join(processed_dir, supplies_filename), index=False)

        if self.dry_run:
            print("Dry run set, not uploading summary table to ArcGIS.")
            status = "Dry run"
        else:
            status = self.gis.overwrite_arcgis_layer("supplies", processed_dir, supplies_filename)
        print(status)
        print("Finished load of supplies data")

    def process_county_summaries(self, processed_dir, processed_filename):

        print("Starting load of county summary table...")

        new_data_filename = "new_county_summary_table.csv"

        df = load_csv_to_df(os.path.join(processed_dir, processed_filename))
        d2 = df.groupby(["HospitalCounty"])[hm.county_sum_columns].sum().reset_index()

        for new_col_name, num_denom in hm.summary_table_header.items():
            d2[new_col_name] = (d2[num_denom["n"]] / d2[num_denom["d"]]) * 100.0
        # PA wants to see 0.0 for any county that doesn't have a hospital, so:
        existing_counties = set(d2["HospitalCounty"].to_list())
        c = Counties()
        all_counties = c.counties
        unused_counties = list(set(all_counties).difference(existing_counties))
        a_row = [0.0] * (len(d2.columns) - 1)
        rows = []
        for county in unused_counties:
            rows.append([county] + a_row)
        row_df = pd.DataFrame(rows, columns=d2.columns)
        d2 = d2.append(row_df)

        d2.to_csv(os.path.join(processed_dir, new_data_filename), header=True, index=False)

        if self.dry_run:
            print("Dry run set, not uploading county summary table to ArcGIS.")
            status = "Dry run"
        else:
            status = self.gis.overwrite_arcgis_layer("county_summaries", processed_dir, new_data_filename)
        print(status)
        print("Finished load of county summary data")

    def process_summaries(self, processed_dir, processed_file_details, make_historical_csv=False):
        print("Starting load of summary table...")

        summary_filename = self.gis.layers['summary_table']['original_file_name']

        summary_df = pd.DataFrame()
        for f in processed_file_details:
            fname = f["processed_filename"]
            size = os.path.getsize(os.path.join(processed_dir, fname))
            if size > 0:
                df = load_csv_to_df(os.path.join(processed_dir, fname))
                table_row = create_summary_table_row(df, f["source_datetime"], f["filename"])
                summary_df = summary_df.append(table_row, ignore_index=True)
            else:
                print(f"{fname} has a filesize of {size}, not processing.")

        if make_historical_csv:
            summary_df.to_csv(summary_filename, index=False, header=True)
            print("Finished creation of historical summary table CSV, returning.")
            return

        layer_conf = self.gis.layers['summary_table']

        # this self.gis.gis.content pattern is evidence that the first pass at
        # a refactored structure should not be the last...
        table = self.gis.gis.content.get(layer_conf['id'])
        t = table.tables[0]

        new_col_names = {}
        for name in t.properties.fields:
            new_col_names[name["alias"]] = name["name"]
        summary_df = summary_df.rename(columns=new_col_names)
        df_as_dict = summary_df.to_dict(orient='records')

        features = []
        for r in df_as_dict:
            ft = Feature(attributes=r)
            features.append(ft)
        # It's okay if features is empty; status will reflect arcgis telling us that,
        # but it won't stop the processing.
        fs = FeatureSet(features)
        if self.dry_run:
            print("Dry run set, not editing features.")
            status = "Dry run"
        else:
            status = t.edit_features(adds=features)
        print(status)
        print("Finished load of summary table")


    def process_historical_hos(self, processed_dir, processed_file_details,  make_historical_csv=False):

        print("Starting load of historical HOS table...")

        layer_conf = self.gis.layers['full_historical_table']
        original_data_file_name = self.gis.layers['full_historical_table']['original_file_name']

        table = self.gis.gis.content.get(layer_conf['id'])
        t = table.layers[0]

        new_col_names = {}
        for name in t.properties.fields:
            new_col_names[name["alias"]]  = name["name"]

        header = {}
        features = []
        hist_csv_rows = []
        for f in processed_file_details:
            fname = f["processed_filename"]
            size = os.path.getsize(os.path.join(processed_dir, fname))
            if size > 0:
                print(f"Adding columns and renaming existing columns for: {fname}")
                processed_time =  datetime.utcnow().isoformat()
                with open(os.path.join(processed_dir, fname), newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        # add our rows
                        hist_csv_row = {}
                        new_row ={}
                        row["Source Data Timestamp"] = f["source_datetime"].isoformat()
                        row["Processed At"] = processed_time
                        row["Source Filename"] = f["filename"]

                        header.update(row)

                        # XXX is this a bug? What happens to headers not in the alias?
                        # rename the headers based on alias
                        for alias, name in new_col_names.items():
                            if alias in row:
                                new_row[name] = row[alias]
                        ft = Feature(attributes=new_row)
                        features.append(ft)
                        hist_csv_rows.append(row)
            else:
                print(f"{fname} has a filesize of {size}, not processing.")

        # historical for generating a new source CSV
        if make_historical_csv:
            if len(hist_csv_rows) > 0:
                with open(os.path.join(processed_dir, original_data_file_name), "w") as csvfile:
                    pprint(list(header.keys()), width=1000)
                    writer = csv.DictWriter(csvfile, fieldnames=set(header.keys()))
                    writer.writeheader()
                    writer.writerows(hist_csv_rows)
        # Done CSV generation

        # It's okay if features is empty; status will reflect arcgis telling us that,
        # but it won't stop the processing.
        fs = FeatureSet(features)
        if self.dry_run:
            print("Dry run set, not editing features.")
            status = "Dry run"
        else:
            fc = len(features)
            chunksize = 1000.0
            feature_batchs = chunks(features, math.ceil(fc / chunksize))
            fb_list = list(feature_batchs)
            fbc = len(fb_list)
            print(f"Adding {fc} features to the historical table in {fbc} batches.")
            for batch in fb_list:
                status = t.edit_features(adds=batch)
                print(status)
        print("Finished load of historical HOS table")

    def process_daily_hospital_averages(self, historical_gis_item_id, daily_averages_item_id):
        # see what days have been processed
        # if not processed, 
        # get the historical table
        # turn it into a df
        # per day, get the averages
        # for new: days
        print("XXX daily_hospital_averages stub, returning.")
        table = self.gis.content.get(historical_gis_item_id)
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
            # rename the columns from the ArcGIS names
            new_col_names = {}
            for name in t.properties.fields:
                new_col_names[name["name"]]  = name["alias"]
            df = df.rename(columns=new_col_names)

            # create a column for the summed tables
            for new_column, cols_to_sum in hm.new_summary_columns.items():
                df[new_column] = df[cols_to_sum].sum()
            old_col_names = list(hm.averages_per_day.values())
            new_col_names = hm.averages_per_day.keys()
            old_col_names.append("HospitalName")
            old_col_names.append("HospitalCounty")
            df.to_csv("one_day_notselected.csv", index=False, header=True)
            df = df[old_col_names]
            df = df.rename(columns=hm.averages_per_day)
            df.to_csv("one_day_selected.csv", index=False, header=True)
            print(df)

    #    new_col_names = {}
    #    for name in t.properties.fields:
    #        new_col_names[name["name"]]  = name["alias"]
    #
    #    df = df.rename(columns=new_col_names)
    #    print(df)
            
            # cut the columns we want out.
            by_hospital_df = df.groupby(["HospitalName"]).mean().reset_index()
            by_hospital_df["Date"] = day
            by_county_df = df.groupby(["HospitalCounty"]).mean().reset_index()
            by_county_df["Date"] = day
            print(by_county_df)
            by_county_df.to_csv("one_day_by_county_avg.csv", index=False, header=True)
            os.exit()

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
