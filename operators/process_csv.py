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

converters = {
    "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-3 or less days Response ?": y_to_one ,
    "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-4-7 days Response ?": y_to_one ,
    "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-8-14 days Response ?": y_to_one,
    "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-15-28 days Response ?": y_to_one,
    "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-29 or more days Response ?": y_to_one,
    "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-3 or less days Response ?": y_to_one,
    "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-4-7 days Response ?": y_to_one,
    "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-8-14 days Response ?": y_to_one,

    "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-8-14 days Response ?": y_to_one,
    "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-15-28 days Response ?": y_to_one,
    "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-29 or more days Response ?": y_to_one,

    "Is there an immediate need for hand hygiene/disinfection supplies listed below?-Disinfection Solutions Response ?": y_to_one,
    "Is there an immediate need for hand hygiene/disinfection supplies listed below?-Disinfection Wipes Response ?": y_to_one,
    "Is there an immediate need for hand hygiene/disinfection supplies listed below?-Gloves Response ?": y_to_one,
    "Is there an immediate need for hand hygiene/disinfection supplies listed below?-Alcohol Based Hand Sanitizer Response ?": y_to_one,
    "Is there an immediate need for hand hygiene/disinfection supplies listed below?-Hand Soap Response ?": y_to_one,
    "At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-4-7 days Response ?": y_to_one,
    "At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-3 or less days Response ?": y_to_one,

    "At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-8-14 days Response ?": y_to_one, 
    "At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-15-28 days Response ?": y_to_one, 
    "At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-29 or more days Response ?": y_to_one,
    }


def normalize_row_keys(row, long_to_short_header):
    # we want to always work with the canonical long names, since that's what Carrie
    # wants. So, we get a row
    new_row = {}
    for k, v in row.items():
        # ArcGIS can't handle ' in header column names.
        if "'" in k:
            k = k.replace("'", "")
        else:
            k = k

        if k in long_to_short_header:
            old_k = k
            k = long_to_short_header[k]

        new_row[k] = v

    return new_row

# accepts a list of files to get (or latest if no list), prefix, column restrictions
# returns a list of files 
def process_csv(file_details, output_dir="/tmp", output_prefix="processed_HOS_", columns_wanted=[]):
    hl = HospitalLocations()
    HM = header_mapping.HeaderMapping("HOS")
    # shortnames to a list of the "canonical" long names
    short_to_canonical_long = HM.get_alias_lookup()
    # longnames to the alias
    long_to_short_header = HM.get_fieldname_lookup()
    # all aliases
    short_to_all_aliases = HM.get_aliases()

    output_file_details = []
    for source_file_details in file_details:
        source_data_file = source_file_details["filename"]
        source_data_dir = source_file_details["dir"]
        output_filename = output_prefix + source_data_file

        source_file_details["processed_filename"] = output_filename
        source_file_details["output_dir"] = output_dir

        output_path = os.path.join(output_dir, output_filename)
        rows = []
        with open (os.path.join(source_data_dir, source_data_file), newline='', encoding="utf8") as rf:
            reader = csv.DictReader(rf)
            # using dictreader, we don't need to read the header row in.
            for row in reader:
                # strip out "'" and also convert to short keys.
                new_row = normalize_row_keys(row, long_to_short_header)
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

                hos_name_key = long_to_short_header["HospitalName"]
                hos_lat_key = long_to_short_header["HospitalLatitude"]
                hos_long_key = long_to_short_header["HospitalLongitude"]
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

