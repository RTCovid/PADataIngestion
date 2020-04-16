import geopy
from geopy.geocoders import Nominatim
import csv

class Counties(object):
    def __init__(self):
        self.cache = {}
        self.counties = self.load_counties()

    def load_counties(self):
        counties = []
        with open("geo_data/pa_counties.csv", newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                counties.append(row[0].title())
        return counties


class HospitalLocations(object):
    # mapping of used names to normalized names
    aliases = { "Ellwood City": "Ellwood City Medical Center",
                "Lancaster General Health-Women & Babies Hospital": "Lancaster General Hospital",
                "AHN-Suburban Hospital": "Lifecare Hospitals of Pittsburgh-North Campus",
                "Hahnemann University Hospital-Transplant Center": "Hahnemann University Hospital",
                "Belmont Center For Comprehensive Treatment": "Belmont Behavioral Hosptial",
                "AHN- Grove City Hospital": "Grove City Medical Center",
                "Riddle Memorial Hopital": "Riddle Memorial Hospital",
                "Riddle Memoial Hospital": "Riddle Memorial Hospital",
                }
    def __init__(self):
        self.cache = {}
        self.cache = self.load_cache()

    def create_error(self, error_string, name, lat, lon):
        error = { }
        error["error"] = error_string
        error["name"] = name
        error["lat"] = lat
        error["lon"] = lon
        return error

    def get_canonical_name(self, hos):
        if hos in self.aliases:
            hos = self.aliases[hos]
        return hos

    def get_location_for_hospital(self, hos):
        if hos in self.cache:
            return self.cache[hos]
        return None

    def load_cache(self):
        cache = {}
        with open("geo_data/geocode_cache.csv", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cache[row["HospitalName"]] = row
        return cache

    def create_new_cache(self, hos_filename):
        locator = Nominatim(user_agent="PAHOS")
        results = []
        errors = []

        pa_hospitals_by_name = {}
        pa_towns_to_counties = {}

        with open("geo_data/pa.csv", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                pa_towns_to_counties[row["Place Name"].lower()] = row["County"].title()

        with open("geo_data/pa_hospitals.csv", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                n = row["Facility ID"]
                n = n.replace('-',' ')
                n = n.replace("'", '')
                n = n.lower()
                pa_hospitals_by_name[n] = row

        with open(hos_filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                result = {}
                error = {}
                name = row["HospitalName"]
                city = row["HospitalCity"]
                state = row["HospitalState"]
                lat = row["HospitalLatitude"]
                lon = row["HospitalLongitude"]
                addr = row["HospitalStreetAddress"]

                result["HospitalName"] = name
                result["HospitalCity"] = city
                result["HospitalState"] = state
                result["HospitalLatitude"] = lat
                result["HospitalLongitude"] = lon
                result["HospitalStreetAddress"] = addr

                result["GeocodedHospitalCounty"] = ""
                result["GeocodedHospitalLocality"] = ""
                result["GeocodedHospitalLocalityType"] = ""
                result["GeocodedHospitalState"] = ""

                n = name.replace('-',' ')
                n = n.replace("'", '')
                n = n.lower()
                print(f"{name}, {lat}, {lon}")
                if n in pa_hospitals_by_name:
                    print("Matched on name")
                    hos = pa_hospitals_by_name[n]
                    result["GeocodedHospitalCounty"] = hos["County Name"].title()
                    result["GeocodedHospitalLocality"] = hos["City"]
                    result["GeocodedHospitalLocalityType"] = "unknown"
                    result["GeocodedHospitalState"] = hos["State"]
                    results.append(result)
                    continue

                if city.lower() in pa_towns_to_counties:
                    print("Matched on city")
                    result["GeocodedHospitalCounty"] = pa_towns_to_counties[city.lower()].title()
                    results.append(result)
                    continue

                if lat == "0" or lon == "0":
                    print(f"{name} has bad lat/lon, skipping")
                    errors.append(self.create_error("bad_lat_lon", name, lat, lon))
                    continue

                l = locator.reverse(f"{lat}, {lon}")
                if "error" in l.raw:
                    print(f"Error geocoding {name} for lat/lon of {lat}, {lon}")
                    errors.append(self.create_error("geocoding", name, lat, lon))
                    continue
                if "county" not in l.raw["address"]:
                    print(f"No county for {name}, skipping")
                    errors.append(self.create_error("no_county", name, lat, lon))
                    continue

                l_county = l.raw["address"]["county"]
                l_state = l.raw["address"]["state"]

                if l_state != "Pennsylvania":
                    print(f"Geocode puts us outside PA for {name}, skipping")
                    errors.append(self.create_error("lat_lon_outside_pa", name, lat, lon))
                    continue

                city_key = "city"
                if "locality" in l.raw["address"]:
                    city_key = "locality"
                elif "village" in l.raw["address"]:
                    city_key = "village"
                elif "town" in l.raw["address"]:
                    city_key = "town"
                elif "hamlet" in l.raw["address"]:
                    city_key = "hamlet"
                else:
                    city_key = None
                if city_key:
                    l_city = l.raw["address"][city_key]
                    result["GeocodedHospitalLocality"] = l_city
                    result["GeocodedHospitalLocalityType"] = city_key
                result["GeocodedHospitalCounty"] = l_county.title()
                result["GeocodedHospitalState"] = l_state


                results.append(result)

        with open ("geo_data/geocode_cache.csv", "w", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

        if errors:
            with open ("geo_data/geocode_errors.csv", "w", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=errors[0].keys())
                writer.writeheader()
                writer.writerows(errors)
# Example:
#h = HospitalLocations()
#h.create_new_cache("processed_HOS_HOS_ResourceCapacity_2020-04-09_15-00.csv")
