import os
import csv
from geo_utils import HospitalLocations
import header_mapping 

def y_to_one(x): 
    if x == "Y":
        return 1
    if x == "N":
        return 0
    return None 


converters = {'n95util1528': y_to_one,
 'n95util29more': y_to_one,
 'n95util814': y_to_one,
 'n95utli3less': y_to_one,
 'n95utli47': y_to_one,
 'needgloves': y_to_one,
 'needhandsoap': y_to_one,
 'needsanitizer': y_to_one,
 'needsolution': y_to_one,
 'needwipes': y_to_one,
 'nputil1528': y_to_one,
 'nputil29more': y_to_one,
 'nputil814': y_to_one,
 'nputli3less': y_to_one,
 'nputli47': y_to_one,
 'ppeutil1528': y_to_one,
 'ppeutil29more': y_to_one,
 'ppeutil814': y_to_one,
 'ppeutli3less': y_to_one,
 'ppeutli47': y_to_one}

def normalize_row_keys(row, master_lookup):
    """transforms the input row's headers to the normalized set, based on the
    input lookup dictionary."""

    new_row = {}

    for k, v in row.items():
        if k in master_lookup:
            new_row[master_lookup[k]] = v

    return new_row

# accepts a list of files to get (or latest if no list), prefix, column restrictions
# returns a list of files
def process_csv(file_details, output_dir="/tmp", output_prefix="processed_HOS_", columns_wanted=[], overwrite=True):
    hl = HospitalLocations()
    HM = header_mapping.HeaderMapping("HOS")
    # shortnames to a list of the "canonical" long names
    # short_to_canonical_long = HM.get_alias_lookup()
    # longnames to the alias
    # long_to_short_header = HM.get_fieldname_lookup()
    # all aliases
    # short_to_all_aliases = HM.get_aliases()
    # just the short names
    # short_header_names = HM.get_fieldnames()

    master_lookup = HM.get_master_lookup()

    output_file_details = []
    for source_file_details in file_details:
        source_data_file = source_file_details["filename"]
        source_data_dir = source_file_details["dir"]
        output_filename = output_prefix + source_data_file

        source_file_details["processed_filename"] = output_filename
        source_file_details["output_dir"] = output_dir
        output_path = os.path.join(output_dir, output_filename)

        if os.path.exists(output_path) and overwrite is False:
            output_file_details.append(source_file_details)
            continue

        rows = []
        with open (os.path.join(source_data_dir, source_data_file), newline='', encoding="utf8") as rf:
            reader = csv.DictReader(rf)
            unmapped_fields = [i for i in reader.fieldnames if i not in master_lookup.keys()]
            if len(unmapped_fields) > 0:
                print(f"{len(unmapped_fields)} unmapped field(s) will be ignored:")
                print("|".join(unmapped_fields))

            for row in reader:
                new_row = normalize_row_keys(row, master_lookup)

                if len(columns_wanted) > 0:
                    ks = list(new_row.keys())
                    for k in ks:
                        if k.strip() not in columns_wanted:
                            del new_row[k]

                for k, v in new_row.items():
                    # Do any value processing here; it'd be nice if we could dataframe.apply() but we can't here.
                    # ArcGIS can't handle ' in header column names.
                    if not k:
                        print(source_data_file)
                        print(new_row)
                    if k in converters:
                        new_row[k] = converters[k](v)
                        v = converters[k](v)

                hos_name_key = master_lookup["HospitalName"]
                hos_lat_key = master_lookup["HospitalLatitude"]
                hos_long_key = master_lookup["HospitalLongitude"]
                hos_county_key = "HospitalCounty"

                # Older files have bad names for hospitals.
                try:
                    new_row[hos_name_key] = hl.get_canonical_name(new_row[hos_name_key])
                except TypeError as e:
                    print(f"{source_data_file}: " + new_row[hos_name_key] + " has no canonical information!")
                    raise e


                # fix bad lat/longs
                try:
                    hos_name = new_row[hos_name_key]
                    loc = hl.get_location_for_hospital(new_row[hos_name_key])
                    new_row[hos_lat_key] = loc["HospitalLatitude"]
                    new_row[hos_long_key] = loc["HospitalLongitude"]

                except TypeError as e:
                    print(f"{source_data_file}: " + new_row[hos_name_key] + " has no location information!")
                    raise e



                # Add the county; future proof in case they add it later
                try:
                    if hos_county_key not in new_row:
                        loc = hl.get_location_for_hospital(new_row[hos_name_key])
                        new_row[hos_county_key] = loc["GeocodedHospitalCounty"]
                except TypeError as e:
                    print(f"{source_data_file}: " + new_row[hos_name_key] + " has no location information!")
                    raise e


                rows.append(new_row)
        with open (output_path, 'w', newline='') as wf:
            writer = csv.DictWriter(wf, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        output_file_details.append(source_file_details)
    return output_file_details

