#!/usr/bin/env python3
from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection, FeatureSet, Table, Feature

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


def get_already_processed_files(gis, item_id):
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
