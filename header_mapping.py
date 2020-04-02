#!/usr/bin/env python3
import pandas as pd

summary_table_header = [
    "Date/Time",
    "Available Beds Adult ICU Staffed",
    "Available Beds Adult ICU",
    "Current Available",
    "% Available Adult ICU Beds",
    "Available Beds Med/Surg Beds Staffed",
    "Available Beds Med/Surg Beds Current Available",
    "% Available Med/Surg Beds",
    "Available Beds Pediatric Intensive Care Staffed",
    "Available Beds Pediatric Intensive Current Available",
    "% Available Beds Pediatric Intensive Care",
    "Available Beds Pediatric Staffed",
    "Available Beds Pediatric Current Available",
    "% Available Pediatric Beds",
    "Other Beds Airborne Infection Isolation Staffed",
    "Other Beds Airborne Infection Isolation Current Available",
    "% Available Airborne Isolation Bed",
]

supplies_on_hand_headers = {
    "3": "Less Than 3 Days",
    "7": "4 to 7 Days",
    "14": "8 to 14 Days",
    "28": "15 to 28 Days",
    "29": "Greater than 29 Days",
}

supplies_types = [
    "N95",
    "PPE",
    "NP Specimen Collection Supplies"
]

columns_to_sum_for_supplies_on_hand = {
    "N95": {
        "3": "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-3 or less days Response ?",
        "7": "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-4-7 days Response ?",
        "14": "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-8-14 days Response ?",
        "28":  "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-15-28 days Response ?",
        "29":  "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-29 or more days Response ?"
    },
    "PPE": {
        "3": "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-3 or less days Response ?",
        "7": "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-4-7 days Response ?",
        "14": "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-8-14 days Response ?",
        "28": "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-15-28 days Response ?",
        "29": "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-29 or more days Response ?"
    },
    "NP Specimen Collection Supplies": {"3": "At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-3 or less days Response ?",
        "7": "At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-4-7 days Response ?",
        "14": "At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-8-14 days Response ?",
        "28": "At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-15-28 days Response ?",
        "29": "At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-29 or more days Response ?"
    }
}
