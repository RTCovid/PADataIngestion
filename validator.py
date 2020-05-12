import os
import csv
from header_mapping import HeaderMapping
from operators.utils import load_geojson


class ValidationError(Exception):
    pass


class CSVValidator():

    def __init__(self, validation_type):

        if validation_type not in ["HOS", "LTC"]:
            raise ValueError("CSVValidator() requires positional argument 'HOS' or 'LTC'")

        self.errors = []
        self.type = validation_type

        hm = HeaderMapping(self.type)
        self.valid_headers = hm.get_fieldnames_and_aliases()

        if self.type == "HOS":
            gj = os.path.join("geo_data", "HOS_locations.geojson")
            self.loc_name_field = "HospitalName"
            self.loc_alias_field = "HospitalNameAliases"
        if self.type == "LTC":
            gj = os.path.join("geo_data", "LTC_locations.geojson")
            self.loc_name_field = "LTCName"
            self.loc_alias_field = "LTCNameAliases"

        self.loc_lookup = load_geojson(gj, self.loc_name_field)

    def validate_locations(self, input_csv):

        location_fails = []
        with open(input_csv, "r", encoding="utf-8") as openf:
            reader = csv.DictReader(openf)

            for row in reader:
                geomatch = None
                name = row[self.loc_name_field].strip()

                # match attempt 1: does the name match?
                if name in self.loc_lookup:
                    geomatch = self.loc_lookup[name]

                # match attempt 2: iterate all possible aliases in lookup
                else:
                    for k, v in self.loc_lookup.items():
                        aliases = v[self.loc_alias_field]
                        if aliases is None:
                            continue
                        if name in aliases.split("|"):
                            geomatch = v
                if geomatch is None:
                    location_fails.append(name)

        result = {
            "pass": len(location_fails) == 0,
            "errors": location_fails
        }
        return result

    def validate_headers(self, input_csv):

        with open(input_csv, "r") as openf:
            reader = csv.reader(openf)
            csv_headers = next(reader)

        result = True
        missing = [i for i in csv_headers if i not in self.valid_headers]
        if len(missing) > 0:
            result = False

        result = {
            "pass": len(missing) == 0,
            "errors": missing
        }
        return result

    def validate_csv(self, input_csv):

        header_result = self.validate_headers(input_csv)
        # location_result = self.validate_locations(input_csv)

        result = {
            "pass": header_result['pass'],# and location_result['pass'],
            "header_errors": header_result['errors'],
            # "location_errors": location_result['errors'],
        }

        return result
