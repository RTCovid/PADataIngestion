import os
import csv
import json
import glob
from datetime import datetime

hos_file = "HOS_locations.geojson"
ltc_file = "LTC_locations.geojson"

full_csv_dir = os.path.join("..", "..", "pa-csv-examples", "all-csvs")

def load_geojson(filename, idfield):
    
    
    with open(filename, "r") as f:
        geojson = json.loads(f.read())

    outdata = {}

    for feature in geojson['features']:
        name = feature['properties'].pop(idfield)
        outdata[name] = feature['properties']
        outdata[name]["long"] = feature['geometry']['coordinates'][0]
        outdata[name]["lat"] = feature['geometry']['coordinates'][1]

    print(f"{len(outdata)} features loaded")
    return outdata

def gather_lat_longs():
    """ needs to be cleaned up before this will really work
    it's just a copy/paste from elsewhere"""
    latlongs_lookup = []
    ltc_lookup = load_geojson(ltc_file, "LTCName")
    ltc_csvs = glob.glob(os.path.join("pa-csv-examples", "all-csvs", "LTC*.csv"))
    
    startdate = datetime.strptime("2020-01-01", "%Y-%m-%d")
    for f in ltc_csvs:

        filename = os.path.splitext(os.path.basename(f))[0]
        d = filename.lstrip("LTC_ResourceCapacity_")[:13]
        ts = datetime.strptime(d, "%Y-%m-%d_%H")
        if ts < startdate:
            continue
        dstr = ts.strftime("%Y-%m-%d %H:%M")

        missing_matches = []
        with open(os.path.abspath(f), "r", encoding="utf8") as openf:
            reader = csv.DictReader(openf)
            for row in reader:
                geomatch = True
                ltc_name = row['LTCName'].strip()
                ltc_lat = row['LTCLatitude'].strip()
                ltc_long = row['LTCLongitude'].strip()
                if ltc_lat not in ["0", ""] and ltc_long not in ["0", ""]:
                    latlongrow = (ltc_name, ltc_lat, ltc_long)
                    latlongs_lookup.append(latlongrow)
    latlongs_unique = list(set(latlongs_lookup))
    latlongs_unique.sort()
    with open("name-lat-long.csv", "w", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(("LTCName","LTCLatitude","LTCLongitude"))
        [writer.writerow(i) for i in latlongs_unique]

def test_ltc_files():

    ltc_lookup = load_geojson(ltc_file, "LTCName")
    ltc_csvs = glob.glob(os.path.join("pa-csv-examples", "all-csvs", "LTC*.csv"))
    
    startdate = datetime.strptime("2020-01-01", "%Y-%m-%d")
    for f in ltc_csvs:

        filename = os.path.splitext(os.path.basename(f))[0]
        d = filename.lstrip("LTC_ResourceCapacity_")[:13]
        ts = datetime.strptime(d, "%Y-%m-%d_%H")
        if ts < startdate:
            continue
        dstr = ts.strftime("%Y-%m-%d %H:%M")

        missing_matches = []
        with open(os.path.abspath(f), "r", encoding="utf8") as openf:
            reader = csv.DictReader(openf)
            for row in reader:
                geomatch = None
                ltc_name = row['LTCName'].strip()

                # match attempt 1: does the name match?
                if ltc_name in ltc_lookup:
                    geomatch = ltc_lookup[ltc_name]

                # match attempt 2: iterate all possible aliases in lookup
                else:
                    for k, v in ltc_lookup.items():
                        aliases = v["LTCNameAliases"]
                        if aliases is None:
                            continue
                        if ltc_name in aliases.split("|"):
                            geomatch = v

                # match attempt 3: sanitized street address (only if there is an address)
                ## NOT CONVINCED THIS IS A GOOD STRATEGY
                if 1 == 2:
                    rowaddress = row['LTCStreetAddress'] + row["LTCCity"]
                    sani_rowaddress = rowaddress.strip().upper().replace(".","")
                    if geomatch is None and sani_rowaddress != "":
                        for k, v in ltc_lookup.items():
                            lookupaddress = v["LTCStreetAddress"] + v["LTCCity"]
                            sani_lookupaddress = lookupaddress.strip().upper().replace(".","")
                            if sani_rowaddress == sani_lookupaddress:
                                # print(f"match on 3: {ltc_name} - {k}")
                                # print(f"{sani_rowaddress} == {sani_lookupaddress}")
                                # print(f"{row['LTCLatitude']} {row['LTCLongitude']} ~ {v['lat']} {v['long']}")
                                geomatch = v
                if geomatch is None:
                    # print(ltc_name)
                    missing_matches.append(f"{ltc_name}: {row['LTCStreetAddress']}")
        print(f"{filename} - {len(missing_matches)}")
        # if len(missing_matches) < 5:
            # print("  "+ "\n  ".join(missing_matches))

def test_hos_files():
    """ only real difference here is "Hospital" vs "LTC"... didn't have time to
    refactor to one function """
    ltc_lookup = load_geojson(hos_file, "HospitalName")
    ltc_csvs = glob.glob(os.path.join(full_csv_dir, "HOS*.csv"))
    
    startdate = datetime.strptime("2020-01-01", "%Y-%m-%d")
    for f in ltc_csvs:

        filename = os.path.splitext(os.path.basename(f))[0]
        d = filename.lstrip("HOS_ResourceCapacity_")[:13]
        ts = datetime.strptime(d, "%Y-%m-%d_%H")
        if ts < startdate:
            continue
        dstr = ts.strftime("%Y-%m-%d %H:%M")

        missing_matches = []
        with open(os.path.abspath(f), "r", encoding="utf8") as openf:
            reader = csv.DictReader(openf)
            for row in reader:
                geomatch = None
                ltc_name = row['HospitalName'].strip()

                # match attempt 1: does the name match?
                if ltc_name in ltc_lookup:
                    geomatch = ltc_lookup[ltc_name]

                # match attempt 2: iterate all possible aliases in lookup
                else:
                    for k, v in ltc_lookup.items():
                        aliases = v["HospitalNameAliases"]
                        if aliases is None:
                            continue
                        if ltc_name in aliases.split("|"):
                            geomatch = v

                # match attempt 3: sanitized street address (only if there is an address)
                ## NOT YET CONVINCED THIS IS A GOOD STRATEGY SO DISABLED FOR NOW
                if 1 == 2:
                    rowaddress = row['HospitalStreetAddress'] + row["HospitalCity"]
                    sani_rowaddress = rowaddress.strip().upper().replace(".","")
                    if geomatch is None and sani_rowaddress != "":
                        for k, v in ltc_lookup.items():
                            lookupaddress = v["HospitalStreetAddress"] + v["HospitalCity"]
                            sani_lookupaddress = lookupaddress.strip().upper().replace(".","")
                            if sani_rowaddress == sani_lookupaddress:
                                # print(f"match on 3: {ltc_name} - {k}")
                                # print(f"{sani_rowaddress} == {sani_lookupaddress}")
                                # print(f"{row['LTCLatitude']} {row['LTCLongitude']} ~ {v['lat']} {v['long']}")
                                geomatch = v
                if geomatch is None:
                    # print(ltc_name)
                    missing_matches.append(f"{ltc_name}: {row['HospitalStreetAddress']}")
        print(f"{filename} - unmatched names: {len(missing_matches)}")
            
            
test_hos_files()