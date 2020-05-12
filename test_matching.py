import os
import csv
import glob
import argparse
import header_mapping as hm
from header_mapping import HeaderMapping
from operators.utils import load_geojson
from validator import CSVValidator

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--dir")
    args = parser.parse_args()

    if args.dir is not None:
        dirpath = args.dir
    else:
        dirpath = "data"

    hos_csvs = glob.glob(os.path.join(dirpath, "HOS*.csv"))
    print(f"validating {len(hos_csvs)} HOS file(s)")
    hos_validator = CSVValidator("HOS")
    for hos in hos_csvs:
        result = hos_validator.validate_csv(hos)
        if result['pass']:
            print(os.path.basename(hos), "pass: True")
        else:
            print(os.path.basename(hos), "pass: False")
            print(f"header errors: {len(result['header_errors'])}")
            for error in result['header_errors']:
                print(f"'{error}'")
            # print(f"location errors: {len(result['location_errors'])}")
            # for error in result['location_errors']:
            #     print(f"'{error}'")
        # print(result)

    # ltc_csvs = glob.glob(os.path.join(dirpath, "LTC*.csv"))
    # print(f"validating {len(ltc_csvs)} LTC file(s)")
    # ltc_validator = CSVValidator("LTC")
    # for ltc in ltc_csvs:
    #     result = ltc_validator.validate_csv(ltc)
