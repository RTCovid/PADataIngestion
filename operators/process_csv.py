import os
import csv
from geo_utils import HospitalLocations
import header_mapping as hm

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

# accepts a list of files to get (or latest if no list), prefix, column restrictions
# returns a list of files 
def process_csv(file_details, output_dir="/tmp", output_prefix="processed_HOS_", columns_wanted=[]):
    hl = HospitalLocations()

    output_file_details = []
    processing_errors = []
    for source_file_details in file_details:
        source_data_file = source_file_details["filename"]
        source_data_dir = source_file_details["dir"]
        output_filename = output_prefix + source_data_file

        source_file_details["processed_filename"] = output_filename
        source_file_details["output_dir"] = output_dir

        output_path = os.path.join(output_dir, output_filename)
        rows = []
        with open (os.path.join(source_data_dir, source_data_file), newline='') as rf:
            reader = csv.DictReader(rf)
            # using dictreader, we don't need to read the header row in.
            for row in reader:
                new_row = {}
                if len(columns_wanted) > 0:
                    ks = list(row.keys())
                    for k in ks:
                        if k.strip() not in columns_wanted:
                            del row[k]
                for k, v in row.items():
                    # Do any value processing here; it'd be nice if we could dataframe.apply() but we can't here.
                    # ArcGIS can't handle ' in header column names.
                    if not k:
                        print(source_data_file)
                        print(row)
                    if k in converters:
                        row[k] = converters[k](v)
                        v = converters[k](v)

                        
                    # ArcGIS can't handle ' in header column names.
                    if "'" in k:
                        new_k = k.replace("'", "")
                    else:
                        new_k = k

                    # fix any misspelled headers
                    if new_k in hm.canonical_headers:
                        msg = f"Found bad key in {source_data_file}: {new_k}"
                        print(msg)
                        processing_errors.append(msg)

                        new_k = hm.canonical_headers[k]

                    new_row[new_k] = v
                    

                # Older files have bad names for hospitals.
                try:
                    new_row["HospitalName"] = hl.get_canonical_name(new_row["HospitalName"])
                except TypeError as e:
                    msg = f"{source_data_file}: " + new_row["HospitalName"] + " has no canonical information!"
                    print(msg)
                    processing_errors.append(msg)

                # fix bad lat/longs
                try:
                    hos_name = new_row["HospitalName"]
                    loc = hl.get_location_for_hospital(new_row["HospitalName"])
                    new_row["HospitalLatitude"] = loc["HospitalLatitude"]
                    new_row["HospitalLongitude"] = loc["HospitalLongitude"]

                except TypeError as e:
                    msg = f"{source_data_file}: " + new_row["HospitalName"] + " has no location information!"
                    print(msg)
                    processing_errors.append(msg)

                # Add the county; future proof in case they add it later
                try:
                    if "HospitalCounty" not in new_row:
                        loc = hl.get_location_for_hospital(new_row["HospitalName"])
                        new_row["HospitalCounty"] = loc["GeocodedHospitalCounty"]
                except TypeError as e:
                    msg = f"{source_data_file}: " + new_row["HospitalName"] + " has no location information!"
                    print(msg)
                    processing_errors.append(msg)

                rows.append(new_row)
        with open (output_path, 'w', newline='') as wf:
            writer = csv.DictWriter(wf, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        output_file_details.append(source_file_details)
    return {'file_details': output_file_details, "errors": processing_errors}
