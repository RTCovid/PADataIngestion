#!/usr/bin/env python3
import pandas as pd


county_sum_columns = [
        "Available Beds-Adult Intensive Care Unit (ICU) Current Available",
        "Available Beds-Medical and Surgical (Med/Surg) Current Available",
        "Available Beds-Pediatric Intensive Care Current Available",
        "Other Beds-Airborne Infection Isolation Current Available",
	"COVID-19 Patient Counts-Total number of patients diagnosed with COVID-19 on ventilators: ",
	"COVID-19 Patient Counts-Total number of patients diagnosed with COVID-19 on ECMO: ",
	"COVID-19 Patient Counts-Total number of inpatients diagnosed with COVID-19: ",
	"Ventilator Counts-Ventilators Number of ventilators",
	"Ventilator Counts-Ventilators Number of ventilators in use",
]

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


columns_for_public_release = [
    "HospitalName",
    "HospitalStreetAddress",
    "HospitalCity",
    "HospitalState",
    "HospitalZip",
    "HospitalLatitude",
    "HospitalLongitude",
    "Available Beds-Adult Intensive Care Unit (ICU) Staffed Beds",
    "Available Beds-Adult Intensive Care Unit (ICU) Current Available",
    "Available Beds-Adult Intensive Care Unit (ICU) 24hr Beds",
    "Available Beds-Adult Intensive Care Unit (ICU) 72hr Beds",
    "Available Beds-Medical and Surgical (Med/Surg) Staffed Beds",
    "Available Beds-Medical and Surgical (Med/Surg) Current Available",
    "Available Beds-Medical and Surgical (Med/Surg) 24hr Beds",
    "Available Beds-Medical and Surgical (Med/Surg) 72hr Beds",
    "Available Beds-Pediatric Intensive Care Staffed Beds",
    "Available Beds-Pediatric Intensive Care Current Available",
    "Available Beds-Pediatric Intensive Care 24hr Beds",
    "Available Beds-Pediatric Intensive Care 72hr Beds",
    "Available Beds-Pediatric Staffed Beds",
    "Available Beds-Pediatric Current Available",
    "Available Beds-Pediatric 24hr Beds",
    "Available Beds-Pediatric 72hr Beds",
    "Other Beds-Airborne Infection Isolation Staffed Beds",
    "Other Beds-Airborne Infection Isolation Current Available",
    "Other Beds-Airborne Infection Isolation 24hr Beds",
    "Other Beds-Airborne Infection Isolation 72hr Beds",
    "COVID-19 Patient Counts-Total number of inpatients diagnosed with COVID-19:",
    "COVID-19 Patient Counts-Total number of inpatients under suspicion for COVID-19 (PUI):",
    "COVID-19 Patient Counts-Total number of patients diagnosed with COVID-19 on ventilators:",
    "COVID-19 Patient Counts-Total number of patients diagnosed with COVID-19 on ECMO:",
    "COVID-19 Patient Counts-How many airborne infection isolation rooms are in your ED?",
    "COVID-19 Patient Counts-How many airborne infection isolation rooms are in your ICU?",
    "COVID-19 Patient Counts-How many airborne infection isolation rooms are in non-ICU?",
    "Ventilator Counts-Ventilators Number of ventilators",
    "Ventilator Counts-Ventilators Number of ventilators in use",
    "Ventilator Counts-Ventilators Number of Anestesia Machines",
    "Ventilator Counts-Ventilators Number of Anestesia Machines that are converted to be used as a Vent",
]

