import os
import csv
from geo_utils import HospitalLocations

# accepts a list of files to get (or latest if no list), prefix, column restrictions
# returns a list of files 
def process_csv(file_details, output_dir="/tmp", output_prefix="processed_HOS_", columns_wanted=[]):
    hl = HospitalLocations()

    output_file_details = []
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
                    # ArcGIS can't handle ' in header column names.
                    if "'" in k:
                        new_k = k.replace("'", "")
                    else:
                        new_k = k
                    new_row[new_k] = v

                # Add the county; future proof in case they add it later
                if "HospitalCounty" not in new_row:
                    new_row["HospitalCounty"] = hl.get_location_for_hospital(new_row["HospitalName"])["GeocodedHospitalCounty"]
                rows.append(new_row)
        with open (output_path, 'w', newline='') as wf:
            writer = csv.DictWriter(wf, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        output_file_details.append(source_file_details)
    return output_file_details

