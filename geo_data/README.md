### Making the LTC location data

The LTC csvs do have lat/long fields, but these are generally empty. Opting to discard those coordinates and geocode all of the addresses instead. Used QGIS and MMQGIS plugin to batch geocode an LTC csv from April 24th. Removed all fields related to capacity reporting and adding a new field (empty for now), called "LTCNameAlias". This field will hold `|` delimited aliases for each facility name (likely to be necessary, if past experience with the hospital is kept in mind).

The input csv had 716 rows (one per reported facility). One row (LTCName: Cheswick Rehabilitation & Wellness Center) was a duplicate, so 715 unique facilities. The geocoding process described above returned 713 matches (a couple of corrections had to be made to poorly formatted addresses).

The 2 missing locations were due to a lack of address in the input csv.

LTCName|
---|
Brookview Health at Menno Haven|
Berwick Retirement Village 2  - Luzerne Co.|

I was able to figure out one, but not the other. The result is 714 facility locations in the output geojson.

#### notes on Menno Haven

This is a facility in Chambersburg, and [this web page](https://mennohaven.org/coronavirus/) describes the location of their two facilities, stating

> Both Menno Haven communities (Brookview on Scotland Avenue and Chambers Pointe on Philadelphia Avenue) are closed to all visitors..."

Looking through the CSV there are actually three entries related to Menno:

LTCName | LTCStreetAddress | my interpretation
--- | --- | ---
Penn Hall at Menno Haven| 1425 Philadelphia Ave. | presumed to be the Chambers Pointe community
Menno-Haven Inc.|2055 Scotland Avenue|this address matches one block away from the Menno Haven on Google Maps. Streetview shows a new facility under construction with a sign saying "Coming Soon: Rehabilitation Center, Menno Haven" etc.
Brookview Health at Menno Haven|<blank>|this is the blank address mentioned above, but coupled with the fact that the Brookview community is mentioned on Scotland Ave. in the website, I will set this address to match the Menno Haven facility on Google Maps, at 2011 Scotland Ave.

Most importantly, in the csv all of these facilities have a distinct set of numbers attached to them, meaning none of them is an inadvertent duplicate of another. So, there are three Menno facilities, and one of them is brand new (2055 Scotland) and one was just missing an address (2011 Scotland).

### notes on Berwick Retirement Village 2 - Luzerne Co.

A separate entry in the csv is

LTCName | LTCStreetAddress | LTCCity
--- | --- | ---
Berwick Retirement Village 1  - Columbia Co.| 801 E. 16th St. | Berwick

This facility matched by address with no problem. I initially assumed that village 2 in Luzerne county would be one of the "other locations" listed in the Commonwealth Health website (which owns/manages Berwick Retirement Village) https://www.commonwealthhealth.net/other-locations. There are a couple of different facilities in Wilkes-Barre, the largest city in Luzerne County, and just up the road from Berwick. On closer inspection, incredibly, the county line on Google Maps runs directly through the health complex at 801 E. 16th St. in Berwick. So "Village 2 - Luzerne Co." could literally be the east wing of "Village 1 - Columbia Co.". I have no idea.

Leaving Village 2 out of the LTC facility data for now. This is unfortunate because village 2 does have numbers reported, while village 1 does not.
