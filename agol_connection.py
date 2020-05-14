from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection, FeatureSet, Table, Feature
import tempfile
import shutil
import json
import csv
import os


class AGOLConnection(object):

    def __init__(self, verbose=False):

        creds = self._load_credentials()
        if creds is None:
            raise Exception("no arcgis credentials supplied")

        self.creds = creds
        self.layers = self._get_layers()
        self.gis = self._make_connection()
        self.verbose = verbose

    def _load_credentials(self):

        cred_path = "creds.csv"
        if not os.path.isfile(cred_path):
            return None

        creds = {}
        with open(cred_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['service'] == 'arcgis':
                    creds['username'] = row['username']
                    creds['password'] = row['password']
                    creds['host'] = row['host']
        return creds

    def _get_layers(self):

        with open("agol_layers.json", "r") as openf:
            configs = json.loads(openf.read())

        return configs

    def _make_connection(self):
        username = self.creds['username']
        password = self.creds['password']
        host = self.creds['host']

        return GIS(host, username, password)

    def get_arcgis_feature_collection_from_item_id(self, arcgis_item_id):

        # You might ask - why do you not just use the FeatureLayerCollection's URL?
        # Because you get a 403 if you try that. Instead, if you grab the parent container
        # from the published layer, you can use the FLC manager's overwrite() method successfully.

        feature_item = self.gis.content.get(arcgis_item_id)
        if "type:Table" in str(feature_item):
            fs = feature_item.tables[0].container
        else:
            fs = feature_item.layers[0].container
        return fs

    def overwrite_arcgis_layer(self, dataset_name, source_data_dir, source_data_file, dry_run=False):

        if self.verbose:
            print(f"Begin upload to ArcGIS Online")
            if dry_run is True:
                print("** DRY RUN -- NO UPLOAD WILL HAPPEN **")

        try:
            layer_config = self.layers[dataset_name]
        except KeyError:
            if self.verbose:
                print(f"Invalid dataset name: {dataset_name}. Valid options are"
                      " {list(self.layers.keys())}. Alter agol_layers.json to add more.")
            return False

        original_file_name = layer_config['original_file_name']
        item_id = layer_config['id']

        if self.verbose:
            print(f"   ArcGIS Online item id: {layer_config['id']}")
            print(f"   CSV name used for upload: {layer_config['original_file_name']}")

        fs = self.get_arcgis_feature_collection_from_item_id(item_id)
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
                            os.path.join(tmpdirname, original_file_name))

            if self.verbose:
                print(f"   local CSV file name: {source_data_dir}/{source_data_file}")
            original_dir = os.getcwd()
            os.chdir(tmpdirname)
            if dry_run is False:
                try:
                    if self.verbose:
                        print("    starting upload...")
                    result = fs.manager.overwrite(original_file_name)
                except Exception as e:
                    if self.verbose:
                        print(f"Caught exception {e} during upload, retrying")
                    result = fs.manager.overwrite(original_file_name)
                if self.verbose:
                    print("        finished.")
            else:
                if self.verbose:
                    result = "Dry run complete"
            os.chdir(original_dir)
        return result

    def get_already_processed_files(self, dataset_name):
        print(f"Getting already processed files for {dataset_name}")

        item_id = self.layers[dataset_name]['id']
        fs = self.gis.content.get(item_id)

        if "type:Table" in str(fs):
            t = fs.tables[0]
        else:
            t = fs.layers[0]

        qr = t.query(
            out_fields='Source_Filename',
            return_geometry=False,  # we don't need the geometries
            return_distinct_values=True,  # get distinct values based on out_fields
            order_by_fields="Source_Filename ASC",  # sort for good measure
        )

        filenames_to_not_sftp = [f.attributes["Source_Filename"] for f in qr.features]
        return filenames_to_not_sftp
