# eventually all of these functions should be migrated into Ingester methods...
from main import process_hospital as process_hospital_old
from main import process_historical_hos as process_historical_hos_old
from main import process_county_summaries as process_county_summaries_old
from main import process_summaries as process_summaries_old
from main import process_daily_hospital_averages as process_daily_hospital_averages_old

import os
import csv
import glob
import pysftp
import pandas as pd
import header_mapping as hm
from operators import process_csv
from operators import get_datetime_from_filename


def load_csv_to_df(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path)
    except UnicodeDecodeError:
        df = pd.read_csv(csv_file_path, encoding='cp1252')
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

class Ingester(object):

    def __init__ (self, dry_run=False):

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
            layer_conf = self.gis.layers['public_feature_layer']
        else:
            layer_conf = self.gis.layers['feature_layer']

        return process_hospital_old(
            self.gis,
            processed_dir,
            processed_filename,
            layer_conf['id'],
            layer_conf['original_file_name'],
            dry_run=self.dry_run
        )

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
            status = self.gis.upload_to_arcgis("supplies", processed_dir, processed_filename)
        print(status)
        print("Finished load of supplies data")

    def process_county_summaries(self, processed_dir, processed_filename):

        return process_county_summaries_old(
            self.gis,
            processed_dir,
            processed_filename,
            self.gis.layers['county_summaries']['id'],
            dry_run=self.dry_run
        )
