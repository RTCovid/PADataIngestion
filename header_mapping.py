#!/usr/bin/env python3
import pandas as pd

summary_table_header = {
    "Percent Available Adult ICU Beds": 
    {
        "n": "Available Beds-Adult Intensive Care Unit (ICU) Current Available",
        "d": "Available Beds-Adult Intensive Care Unit (ICU) Staffed Beds" ,
    },
    "Percent Available Med/Surg Beds": 
    {
        "n": "Available Beds-Medical and Surgical (Med/Surg) Current Available",
        "d": "Available Beds-Medical and Surgical (Med/Surg) Staffed Beds",
    },
    "Percent Available Beds Pediatric Intensive Care":
    {
        "n": "Available Beds-Pediatric Intensive Care Current Available",
        "d": "Available Beds-Pediatric Intensive Care Staffed Beds",
    },
    "Percent Available Pediatric Beds": {
        "n": "Available Beds-Pediatric Current Available",
        "d": "Available Beds-Pediatric Staffed Beds",
    },
    "Percent Available Airborne Isolation Bed": 
    {
        "n": "Other Beds-Airborne Infection Isolation Current Available",
        "d": "Other Beds-Airborne Infection Isolation Staffed Beds",
    }
}

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
