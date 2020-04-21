#!/usr/bin/env python3
import pandas as pd


county_sum_columns = [
        "HospitalCounty",
        "Available Beds-Adult Intensive Care Unit (ICU) Current Available",
        "Available Beds-Adult Intensive Care Unit (ICU) Staffed Beds",
        "Available Beds-Medical and Surgical (Med/Surg) Current Available",
        "Available Beds-Medical and Surgical (Med/Surg) Staffed Beds",
        "Available Beds-Pediatric Intensive Care Current Available",
        "Available Beds-Pediatric Intensive Care Staffed Beds",
        "Available Beds-Pediatric Current Available",
        "Available Beds-Pediatric Staffed Beds",
        "Other Beds-Airborne Infection Isolation Current Available",
        "Other Beds-Airborne Infection Isolation Staffed Beds",
	"COVID-19 Patient Counts-Total number of inpatients diagnosed with COVID-19 on ventilators: ",
	"COVID-19 Patient Counts-Total number of inpatients diagnosed with COVID-19 on ECMO: ",
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


new_summary_columns = {
    "N95 masks >7 days": [ 
	"At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-8-14 days Response ?",
        "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-15-28 days Response ?", 
	"At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-29 or more days Response ?"],
    "PPE >7 days": [ 
	"At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-8-14 days Response ?", 
	"At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-15-28 days Response ?", 
	"At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-29 or more days Response ?",
     ],
    "NP Specimen Collection Supplies >7 days": [ 
	"At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-8-14 days Response ?",
	"At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-15-28 days Response ?",
	"At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-29 or more days Response ?",
    ],
}

averages_per_day = {
    "COVID-19 Inpatients average per day": "COVID-19 Patient Counts-Total number of inpatients diagnosed with COVID-19:",
    "COVID-19 patients on ventilators average per day": "COVID-19 Patient Counts-Total number of patients diagnosed with COVID-19 on ventilators:",
    "Ventilators available average per day": "Ventilator Counts-Ventilators Number of ventilators",
    "Ventilators in use average per day": "Ventilator Counts-Ventilators Number of ventilators in use",
    "Adult ICU Beds Current Available average per day" :"Available Beds-Adult Intensive Care Unit (ICU) Current Available",
    "Med/Surg Beds Current Available average per day" :"Available Beds-Medical and Surgical (Med/Surg) Current Available",
    "Other Beds – Airborne Isolation Infection Room Beds Current Available average per day":"Other Beds-Airborne Infection Isolation Current Available",
    "Employees absent average per day":"Employee Status-Total Employee Call Outs/Absenteeism",
    "Employees absent child care issues average per day":"Employee Status-Call out reason: child care issues",
    "Employees absent COVID19 infection average per day":"Employee Status-Call out reason: sick with COVID-19",
    "Employees absent quarantine isolation average per day":"Employee Status-Call out reason: quarantine or isolation due to exposure",
    "N95 masks <3 days average count per day":"At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-3 or less days Response ?",
    "N95 masks 4-7 days average count per day":"At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-4-7 days Response ?",
    "N95 masks >7 days average count per day": "N95 masks >7 days",
    "PPE <3 days average count per day":"At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-3 or less days Response ?",
    "PPE 4-7 days average count per day":"At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-4-7 days Response ?",
    "PPE >7 days average count per day": "PPE >7 days",
    "NP Specimen Collection Supplies <3 days average count per day":"At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-3 or less days Response ?",
    "NP Specimen Collection Supplies 4-7 days average count per day": "At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-4-7 days Response ?", 
    "NP Specimen Collection Supplies >7 days average count per day": "NP Specimen Collection Supplies >7 days",
    "Immediate need disinfection solution average count per day":"Is there an immediate need for hand hygiene/disinfection supplies listed below?-Disinfection Solutions Response ?",
    "Immediate need disinfection wipes average count per day":"Is there an immediate need for hand hygiene/disinfection supplies listed below?-Disinfection Wipes Response ?",
    "Immediate need gloves average count per day":"Is there an immediate need for hand hygiene/disinfection supplies listed below?-Gloves Response ?",
    "Immediate need hand sanitizer average count per day":"Is there an immediate need for hand hygiene/disinfection supplies listed below?-Alcohol Based Hand Sanitizer Response ?",
    "Immediate need hand soap average count per day":"Is there an immediate need for hand hygiene/disinfection supplies listed below?-Hand Soap Response ?",
}

avg_to_do = [
    "% Adult ICU Beds Current Available average per day (Available/staffed)*100",
    "% Med/Surg Beds Current Available average per day (Available/staffed)*100",
    "% Other Beds – Airborne Isolation Infection Room Beds Current Available average per day (Available/staffed)*100",
]
