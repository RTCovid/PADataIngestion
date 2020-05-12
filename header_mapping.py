#!/usr/bin/env python3

class HeaderMapping(object):
    """Instantiate with either "HOS" or "LTC" to get header utils for each type
    of CSV."""

    def __init__(self, mapping_type):
        if mapping_type == "HOS":
            self.mapping = hos_mapping
        elif mapping_type == "LTC":
            self.mapping = ltc_mapping
        else:
            raise ValueError("HeaderMapping() requires positional argument 'HOS' or 'LTC'")

    def get_fieldname_lookup(self):
        """This lookup has aliases as keys and their corresponding short
        fieldnames as values."""

        lookup = {}
        for k, v in self.mapping.items():
            for alias in v:
                lookup[alias] = k

        return lookup

    def get_alias_lookup(self):
        """This lookup has short fieldnames as keys and their preferred aliases
        as values. Preferred alias is the first in the list in hos_mapping."""

        lookup = {}
        for k, v in self.mapping.items():
            lookup[k] = v[0]

        return lookup

    def get_aliases(self):
        """This is a list of all valid aliases. Most useful for testing."""

        values = []
        for v in self.mapping.values():
            values += v
        return values

    def get_fieldnames(self):
        """This is a list of all valid short fieldnames. Most useful for testing."""

        return list(self.mapping.keys())

    def get_fieldnames_and_aliases(self):
        """Creates one big list of all fieldnames and all aliases."""

        return self.get_fieldnames() + self.get_aliases()


ltc_mapping = {}

columns_for_public_release = ['hospitalname',
 'hospitalstreetaddress',
 'hospitalcity',
 'hospitalstate',
 'hospitalzip',
 'hospitallatitude',
 'hospitallongitude',
 'numicubeds',
 'icuavail',
 'icu24h',
 'icu72h',
 'medsurgstaff',
 'medsurgavail',
 'medsurg24h',
 'medsurg72h',
 'picstaff',
 'picavail',
 'pic24h',
 'pic72h',
 'pedstaff',
 'pedavail',
 'ped24h',
 'ped72h',
 'aiistaff',
 'aiiavail',
 'aii24h',
 'aii72h',
 'numc19hosppats',
 'ttlcvd19pui',
 'numc19mechventpats',
 'ttlcvd19ptntecmo',
 'ttlaiied',
 'ttlaiiicu',
 'ttlaiinonicu',
 'numvent',
 'numventuse',
 'numanesthesia',
 'numanesthesiaconvert']
hos_mapping = {
    'hospitalname': [
        'HospitalName',
        'hospitalName',
    ],
    'hospitalstreetaddress': [
        'HospitalStreetAddress',
        'hospitalStreetAddress',
    ],
    'hospitalcity': [
        'HospitalCity',
        'hospitalCity',
    ],
    'hospitalstate': [
        'HospitalState',
        'hospitalState',
    ],
    'hospitalzip': [
        'HospitalZip',
        'hospitalZip',
    ],
    'hospitallatitude': [
        'HospitalLatitude',
        'hospitalLatitude',
    ],
    'hospitallongitude': [
        'HospitalLongitude',
        'hospitalLongitude',
    ],
    'numicubeds': [
        'Available Beds-Adult Intensive Care Unit (ICU) Staffed Beds',
    ],
    'icuavail': [
        'Available Beds-Adult Intensive Care Unit (ICU) Current Available',
    ],
    'icu24h': [
        'Available Beds-Adult Intensive Care Unit (ICU) 24hr Beds',
    ],
    'icu72h': [
        'Available Beds-Adult Intensive Care Unit (ICU) 72hr Beds',
    ],
    'medsurgstaff': [
        'Available Beds-Medical and Surgical (Med/Surg) Staffed Beds',
    ],
    'medsurgavail': [
        'Available Beds-Medical and Surgical (Med/Surg) Current Available',
    ],
    'medsurg24h': [
        'Available Beds-Medical and Surgical (Med/Surg) 24hr Beds',
    ],
    'medsurg72h': [
        'Available Beds-Medical and Surgical (Med/Surg) 72hr Beds',
    ],
    'burnstaff': [
        'Available Beds-Burn Staffed Beds',
    ],
    'burnavail': [
        'Available Beds-Burn Current Available',
    ],
    'burn24h': [
        'Available Beds-Burn 24hr Beds',
    ],
    'burn72h': [
        'Available Beds-Burn 72hr Beds',
    ],
    'picstaff': [
        'Available Beds-Pediatric Intensive Care Staffed Beds',
    ],
    'picavail': [
        'Available Beds-Pediatric Intensive Care Current Available',
    ],
    'pic24h': [
        'Available Beds-Pediatric Intensive Care 24hr Beds',
    ],
    'pic72h': [
        'Available Beds-Pediatric Intensive Care 72hr Beds',
    ],
    'pedstaff': [
        'Available Beds-Pediatric Staffed Beds',
    ],
    'pedavail': [
        'Available Beds-Pediatric Current Available',
    ],
    'ped24h': [
        'Available Beds-Pediatric 24hr Beds',
    ],
    'ped72h': [
        'Available Beds-Pediatric 72hr Beds',
    ],
    'nicustaff': [
        'Available Beds-Neonatal Staffed Beds',
    ],
    'nicuavail': [
        'Available Beds-Neonatal Current Available',
    ],
    'nicu24h': [
        'Available Beds-Neonatal 24hr Beds',
    ],
    'nicu72h': [
        'Available Beds-Neonatal 72hr Beds',
    ],
    'rehabstaff': [
        'Available Beds-Inpatient Rehab Staffed Beds',
    ],
    'rehabavail': [
        'Available Beds-Inpatient Rehab Current Available',
    ],
    'rehab24h': [
        'Available Beds-Inpatient Rehab 24hr Beds',
    ],
    'rehab72h': [
        'Available Beds-Inpatient Rehab 72hr Beds',
    ],
    'psychstaff': [
        'Psych Beds-Psychiatric Staffed Beds',
    ],
    'psychavail': [
        'Psych Beds-Psychiatric Current Available',
    ],
    'psych24h': [
        'Psych Beds-Psychiatric 24hr Beds',
    ],
    'psych72h': [
        'Psych Beds-Psychiatric 72hr Beds',
    ],
    'psychadultstaff': [
        'Psych Beds-Adult Staffed Beds',
    ],
    'psychadultavail': [
        'Psych Beds-Adult Current Available',
    ],
    'psychadult24h': [
        'Psych Beds-Adult 24hr Beds',
    ],
    'psychadult72h': [
        'Psych Beds-Adult 72hr Beds',
    ],
    'psychadolstaff': [
        'Psych Beds-Adolescent Staffed Beds',
    ],
    'psychadolavail': [
        'Psych Beds-Adolescent Current Available',
    ],
    'psychadol24h': [
        'Psych Beds-Adolescent 24hr Beds',
    ],
    'psychadol72h': [
        'Psych Beds-Adolescent 72hr Beds',
    ],
    'psychgeristaff': [
        'Psych Beds-Geriatric Staffed Beds',
    ],
    'psychgeriavail': [
        'Psych Beds-Geriatric Current Available',
    ],
    'psychgeri24h': [
        'Psych Beds-Geriatric 24hr Beds',
    ],
    'psychgeri72h': [
        'Psych Beds-Geriatric 72hr Beds',
    ],
    'psychmeddetoxstaff': [
        'Psych Beds-Medical Detox Staffed Beds',
    ],
    'psychmeddetoxavail': [
        'Psych Beds-Medical Detox Current Available',
    ],
    'psychmeddetox24h': [
        'Psych Beds-Medical Detox 24hr Beds',
    ],
    'psychmeddetox72h': [
        'Psych Beds-Medical Detox 72hr Beds',
    ],
    'psychsaddstaff': [
        'Psych Beds-Substance Abuse (Dual Diagnosis) Staffed Beds',
    ],
    'psychsaddavail': [
        'Psych Beds-Substance Abuse (Dual Diagnosis) Current Available',
    ],
    'psychsadd24h': [
        'Psych Beds-Substance Abuse (Dual Diagnosis) 24hr Beds',
    ],
    'psychsadd72h': [
        'Psych Beds-Substance Abuse (Dual Diagnosis) 72hr Beds',
    ],
    'labordelivstaff': [
        'Other Beds-Labor / Delivery Staffed Beds',
    ],
    'labordelivavail': [
        'Other Beds-Labor / Delivery Current Available',
    ],
    'labordeliv24h': [
        'Other Beds-Labor / Delivery 24hr Beds',
    ],
    'labordeliv72h': [
        'Other Beds-Labor / Delivery 72hr Beds',
    ],
    'maternitystaff': [
        'Other Beds-Maternity / Newborn Nursery Staffed Beds',
    ],
    'maternityavail': [
        'Other Beds-Maternity / Newborn Nursery Current Available',
    ],
    'maternity24h': [
        'Other Beds-Maternity / Newborn Nursery 24hr Beds',
    ],
    'maternity72h': [
        'Other Beds-Maternity / Newborn Nursery 72hr Beds',
    ],
    'aiistaff': [
        'Other Beds-Airborne Infection Isolation Staffed Beds',
    ],
    'aiiavail': [
        'Other Beds-Airborne Infection Isolation Current Available',
    ],
    'aii24h': [
        'Other Beds-Airborne Infection Isolation 24hr Beds',
    ],
    'aii72h': [
        'Other Beds-Airborne Infection Isolation 72hr Beds',
    ],
    'edimmediate': [
        'Emergency Department-ED Available Capacity Immediate',
    ],
    'eddelayed': [
        'Emergency Department-ED Available Capacity Delayed',
    ],
    'edminor': [
        'Emergency Department-ED Available Capacity Minor',
    ],
    'eddeceased': [
        'Emergency Department-ED Available Capacity Deceased',
    ],
    'noncvd19pntadmit': [
        'Admission Data-Number of Patients awaiting admission Non COVID-19 Response ?',
        'Admission Data-Number of Patients awaiting admission Response ?',
    ],
    'cvd19pntadmitnonvent': [
        'Admission Data-Number of Patients awaiting admission with Confirmed or PUI COVID-19 non-ventilated Response ?',
        'Admission Data-Number of Patients awaiting admission with Confirmed or PUI COVID19 non-ventilated Response ?',
    ],
    'cvd19pntadmitnvent': [
        'Admission Data-Number of Patients awaiting admission for Confirmed or PUI COVID-19 on ventilator Response ?',
        'Admission Data-Number of Patients awaiting admission for Confirmed or PUI COVID 19 on ventilator Response ?',
    ],
    'pntadmiticu': [
        'Admission Data-Number of Patients awaiting ICU Bed Response ?',
    ],
    'pntdischrg': [
        'Admission Data-Number of Patients awaiting discharge placement Response ?',
    ],
    'facrespplan': [
        'EEIs-Does your facility have an established respiratory protection plan? Response ?',
    ],
    'n95fittested': [
        'EEIs-Is your facility planning to use N95 masks. If so is your staff fit-tested to wear N95 masks? Response ?',
    ],
    'modelsfittested': [
        'EEIs-What mask brands and models are staff fit tested to use? Response ?',
    ],
    'paprtrained': [
        'EEIs-Is your facility planning to use PAPRs. If so is your staff trained to use PAPRs? Response ?',
    ],
    'ppedondoff': [
        'EEIs-Is your staff adequately trained in correctly donning and doffing of PPE? Response ?',
    ],
    'needsanitizer': [
        'Is there an immediate need for hand hygiene/disinfection supplies listed below?-Alcohol Based Hand Sanitizer Response ?',
    ],
    'needhandsoap': [
        'Is there an immediate need for hand hygiene/disinfection supplies listed below?-Hand Soap Response ?',
    ],
    'needsolution': [
        'Is there an immediate need for hand hygiene/disinfection supplies listed below?-Disinfection Solutions Response ?',
    ],
    'needwipes': [
        'Is there an immediate need for hand hygiene/disinfection supplies listed below?-Disinfection Wipes Response ?',
    ],
    'needgloves': [
        'Is there an immediate need for hand hygiene/disinfection supplies listed below?-Gloves Response ?',
    ],
    'needother1': [
        'Is there an immediate need for hand hygiene/disinfection supplies listed below?-Other (please specify) Response ?',
    ],
    'needn95': [
        "Does your facility anticipate material/supply shortages of the following?-N95's Response ?",
    ],
    'needpapr': [
        "Does your facility anticipate material/supply shortages of the following?-PAPR's Response ?",
    ],
    'needpaprhoods': [
        "Does your facility anticipate material/supply shortages of the following?-PAPR's Hoods Response ?",
    ],
    'needpaprfilters': [
        "Does your facility anticipate material/supply shortages of the following?-PAPR's Filters Response ?",
    ],
    'needmasks': [
        'Does your facility anticipate material/supply shortages of the following?-Facial Masks (Procedural/Surgical) Response ?',
    ],
    'needgown': [
        'Does your facility anticipate material/supply shortages of the following?-Gown/Apron Response ?',
    ],
    'needeyepro': [
        'Does your facility anticipate material/supply shortages of the following?-Eye Protection (Goggles Face shield) Response ?',
    ],
    'needcleaning': [
        'Does your facility anticipate material/supply shortages of the following?-Cleaning/Disinfection Supplies Response ?',
    ],
    'needother2': [
        'Does your facility anticipate material/supply shortages of the following?-Other (please specify) Response ?',
    ],
    'shortn95': [
        "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-N95's Response ?",
    ],
    'shortpapr': [
        "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-PAPR's Response ?",
    ],
    'shortpaprhoods': [
        "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-PAPR's Hoods Response ?",
    ],
    'shortpaprfilters': [
        "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-PAPR's Filters Response ?",
    ],
    'shortmasks': [
        'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Facial Masks (Procedural/Surgical) Response ?',
    ],
    'shortgowns': [
        'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Gowns Response ?',
    ],
    'shorteyepro': [
        'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Eye Protection (Goggles Face shield) Response ?',
    ],
    'shortsoap': [
        'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Hand Soap Response ?',
    ],
    'shortsanitizer': [
        'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Hand Sanitizer Response ?',
    ],
    'shortcleaning': [
        'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Cleaning/Disinfection Supplies Response ?',
    ],
    'shortother1': [
        'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Other (please specify) Response ?',
    ],
    'burnn95': [
        "Current Burn Rates per day for the following PPE (Single Units):-N95's Response ?",
    ],
    'burnpapr': [
        "Current Burn Rates per day for the following PPE (Single Units):-PAPR's Response ?",
    ],
    'burnpaprhoods': [
        "Current Burn Rates per day for the following PPE (Single Units):-PAPR's Hoods Response ?",
    ],
    'burnpaprfilter': [
        "Current Burn Rates per day for the following PPE (Single Units):-PAPR's Filters Response ?",
    ],
    'burnmask': [
        'Current Burn Rates per day for the following PPE (Single Units):-Facial Masks (Procedural/Surgical) Response ?',
    ],
    'burngowns': [
        'Current Burn Rates per day for the following PPE (Single Units):-Gowns Response ?',
    ],
    'burneyepro': [
        'Current Burn Rates per day for the following PPE (Single Units):-Eye Protection (Goggles Face shield) Response ?',
    ],
    'shortcollection': [
        'Testing Supplies-What diagnostic testing or specimen collection supplies do you anticipate a shortage of? ',
    ],
    'shortother2': [
        'Testing Supplies-Other (please specify) ',
    ],
    'testlocal': [
        'Local Testing-Do you have a commercial or inhouse platform for performing local testing of COVID-19? ',
    ],
    'date': [
        'Local Testing-Real or future go-live date: ',
    ],
    'cvd19tstrun': [
        'Local Testing-How many COVID-19 tests were run at your inhouse lab today? ',
        'How many COVID-19 tests were run at your inhouse lab today? ',
    ],
    'cvd19tstpostve': [
        'Local Testing-How many of those inhouse tests were positive? ',
        'How many of those inhouse tests were positive? ',
    ],
    'numc19hosppats': [
        'COVID-19 Patient Counts-Total number of inpatients diagnosed with COVID-19: ',
        'COVID-19 Patient Counts-Total number of inpatients diagnosed with COVID-19:',
    ],
    'ttlcvd19pui': [
        'COVID-19 Patient Counts-Total number of inpatients under suspicion for COVID-19 (PUI): ',
        'COVID-19 Patient Counts-Total number of inpatients under suspicion for COVID-19 (PUI):',
    ],
    'ttlnumicubedscvd19': [
        'COVID-19 Patient Counts - Total number of ICU beds occupied by a diagnosed COVID-19 patient:',
        'COVID-19 Patient Counts-Total number of ICU beds occupied by a diagnosed COVID-19 patient: ',
        'COVID-19 Patient Counts-Total number of ICU beds occupied by a diagnosed COVID-19 patient:',
    ],
    'cvdnumc19hopats': [
        'COVID-19 Patient Counts-Total number of inpatients admitted 14+ days for other conditions now PUI or confirmed COVID-19?: ',
        'COVID-19 Patient Counts-Total number of inpatients admitted 14+ days for other conditions now PUI or confirmed COVID-19?:',
    ],
    'numc19mechventpats': [
        'COVID-19 Patient Counts-Total number of inpatients diagnosed with COVID-19 on ventilators: ',
        'COVID-19 Patient Counts-Total number of patients diagnosed with COVID-19 on ventilators: ',
        'COVID-19 Patient Counts-Total number of patients diagnosed with COVID-19 on ventilators:',
    ],
    'ttlcvd19ptntecmo': [
        'COVID-19 Patient Counts-Total number of inpatients diagnosed with COVID-19 on ECMO: ',
        'COVID-19 Patient Counts-Total number of patients diagnosed with COVID-19 on ECMO: ',
        'COVID-19 Patient Counts-Total number of patients diagnosed with COVID-19 on ECMO:',
    ],
    'ttlaiied': [
        'COVID-19 Patient Counts-How many airborne infection isolation rooms are in your ED? ',
        'COVID-19 Patient Counts-How many airborne infection isolation rooms are in your ED?',
    ],
    'ttlaiiicu': [
        'COVID-19 Patient Counts-How many airborne infection isolation rooms are in your ICU? ',
        'COVID-19 Patient Counts-How many airborne infection isolation rooms are in your ICU?',
    ],
    'ttlaiinonicu': [
        'COVID-19 Patient Counts-How many airborne infection isolation rooms are in non-ICU? ',
        'COVID-19 Patient Counts-How many airborne infection isolation rooms are in non-ICU?',
    ],
    'cvdnumc19died': [
        'COVID-19 Patient Counts-Number of patient deaths with Confirmed or PUI for COVID-19 in last 24 hours: ',
        'COVID-19 Patient Counts-Number of patient deaths with Confirmed or PUI for COVID 19 in last 24 hours: ',
        'COVID-19 Patient Counts-Number of patient deaths with Confirmed or PUI for COVID 19 in last 24 hours:',
    ],
    'conspperesp': [
        'Are you currently implementing conservation strategies to preserve PPE:-Extended use of respirators Response ?',
    ],
    'consppereuseresp': [
        'Are you currently implementing conservation strategies to preserve PPE:-Use of reusable respirators in place of disposable N95s (i.e. PAPRs elastomeric N95s etc.) Response ?',
    ],
    'consppedispon95': [
        'Are you currently implementing conservation strategies to preserve PPE:-Reuse of disposable N95 respirators Response ?',
    ],
    'consppestaffhours': [
        'Are you currently implementing conservation strategies to preserve PPE:-Extended staff hours/shifts Response ?',
    ],
    'consppecohortwodestaff': [
        'Are you currently implementing conservation strategies to preserve PPE:-Cohorting patients without dedicated staff Response ?',
    ],
    'consppecohortwdestaff': [
        'Are you currently implementing conservation strategies to preserve PPE:-Cohorting patients with dedicated staff Response ?',
    ],
    'n95utli3less': [
        'At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-3 or less days Response ?',
    ],
    'n95utli47': [
        'At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-4-7 days Response ?',
    ],
    'n95util814': [
        'At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-8-14 days Response ?',
    ],
    'n95util1528': [
        'At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-15-28 days Response ?',
    ],
    'n95util29more': [
        'At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-29 or more days Response ?',
    ],
    'ppeutli3less': [
        'At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-3 or less days Response ?',
    ],
    'ppeutli47': [
        'At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-4-7 days Response ?',
    ],
    'ppeutil814': [
        'At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-8-14 days Response ?',
    ],
    'ppeutil1528': [
        'At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-15-28 days Response ?',
    ],
    'ppeutil29more': [
        'At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-29 or more days Response ?',
    ],
    'nputli3less': [
        'At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-3 or less days Response ?',
    ],
    'nputli47': [
        'At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-4-7 days Response ?',
    ],
    'nputil814': [
        'At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-8-14 days Response ?',
    ],
    'nputil1528': [
        'At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-15-28 days Response ?',
    ],
    'nputil29more': [
        'At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-29 or more days Response ?',
    ],
    'ttlempcall': [
        'Employee Status-Total Employee Call Outs/Absenteeism ',
    ],
    'ttlempcvd19': [
        'Employee Status-Call out reason: sick with COVID-19 ',
    ],
    'ttlcalloutphys': [
        'Employee Status-Number of Call Outs that are Physicians ',
    ],
    'ttlcalloutnurse': [
        'Employee Status-Number of Call Outs that are Nurses ',
    ],
    'ttlcalloutisolation': [
        'Employee Status-Call out reason: quarantine or isolation due to exposure ',
    ],
    'ttlcalloutchildcare': [
        'Employee Status-Call out reason: child care issues ',
    ],
    'envrnmntlsrvcsday': [
        'Critical Staffing Shortages Today?-Environmental Services Response ?',
        'Todays Critical Staffing Shortages - Environmental Services',
    ],
    'rnlpnday': [
        'Critical Staffing Shortages Today?-Nurses: RN and LPNs Response ?',
        'Todays Critical Staffing Shortages -Nurses: RN and LPNs',
    ],
    'rsprtrythrpstday': [
        'Critical Staffing Shortages Today?-Respritory Therapists Response ?',
        'Todays Critical Staffing Shortages -Respritory Therapists',
    ],
    'phtmcstday': [
        'Critical Staffing Shortages Today?-Pharmacists and Pharmacy Techs Response ?',
        'Todays Critical Staffing Shortages -Pharmacists and Pharmacy Techs',
    ],
    'physcnstday': [
        'Critical Staffing Shortages Today?-Physicans: Attending Fellows Response ?',
        'Todays Critical Staffing Shortages -Physicans: Attending, Fellows',
    ],
    'otherindpendtday': [
        'Critical Staffing Shortages Today?-Other licensed independent practitioners: Advanced Practice Nurses Physician Assistances Response ?',
        'Todays Critical Staffing Shortages -Other licensed independent practitioners: Advanced Practice Nurses, Physician Assistances',
    ],
    'tempday': [
        'Critical Staffing Shortages Today?-Temporary physicians nurse etc (per diems travelers retired seasonal) Response ?',
        'Todays Critical Staffing Shortages -Temporary physicians, nurse, etc (per diems, travelers, retired, seasonal)',
    ],
    'otherhcpday': [
        'Critical Staffing Shortages Today?-Other HCP Personnel (Other persons who work in the facilities not detailed above Response ?',
        'Todays Critical Staffing Shortages -Other HCP Personnel (Other persons who work in the facilities not detailed above',
    ],
    'otherhcpdaylist': [
        'Critical Staffing Shortages Today?-What other HCP Personnel not listed above do you have a critical staff shortage of? Response ?',
        'Todays Critical Staffing Shortages -What other HCP Personnel not listed above do you have a critical staff shortage of? ',
    ],
    'envrnmntlsrvcsweek': [
        'Critical Staffing Shortages within a week?-Environmental Services Response ?',
        'Forecasted Critical Staffing Shortages - Environmental Services',
    ],
    'rnlpnweek': [
        'Critical Staffing Shortages within a week?-Nurses: RN and LPNs Response ?',
        'Forecasted Critical Staffing Shortages -Nurses: RN and LPNs',
    ],
    'rsprtrythrpstweek': [
        'Critical Staffing Shortages within a week?-Respritory Therapists Response ?',
        'Forecasted Critical Staffing Shortages -Respritory Therapists',
    ],
    'phtmcstweek': [
        'Critical Staffing Shortages within a week?-Pharmacists and Pharmacy Techs Response ?',
        'Forecasted Critical Staffing Shortages -Pharmacists and Pharmacy Techs',
    ],
    'physcnstweek': [
        'Critical Staffing Shortages within a week?-Physicans: Attending Fellows Response ?',
        'Forecasted Critical Staffing Shortages -Physicans: Attending, Fellows',
    ],
    'otherindpendtweek': [
        'Critical Staffing Shortages within a week?-Other licensed independent practitioners: Advanced Practice Nurses Physician Assistances Response ?',
        'Forecasted Critical Staffing Shortages -Other licensed independent practitioners: Advanced Practice Nurses, Physician Assistances',
    ],
    'tempweek': [
        'Critical Staffing Shortages within a week?-Temporary physicians nurse etc (per diems travelers retired seasonal) Response ?',
        'Forecasted Critical Staffing Shortages -Temporary physicians, nurse, etc (per diems, travelers, retired, seasonal)',
    ],
    'otherhcpweek': [
        'Critical Staffing Shortages within a week?-Other HCP Personnel (Other persons who work in the facilities not detailed above Response ?',
        'Forecasted Critical Staffing Shortages -Other HCP Personnel (Other persons who work in the facilities not detailed above',
    ],
    'otherhcpweeklist': [
        'Critical Staffing Shortages within a week?-What other HCP Personnel not listed above do you have a critical staff shortage of? Response ?',
        'Forecasted Critical Staffing Shortages -What other HCP Personnel not listed above do you have a critical staff shortage of? ',
    ],
    'numvent': [
        'Ventilator Counts-Ventilators Number of ventilators',
    ],
    'numventuse': [
        'Ventilator Counts-Ventilators Number of ventilators in use',
    ],
    'numanesthesia': [
        'Ventilator Counts-Ventilators Number of Anesthesia Machines',
        'Ventilator Counts-Ventilators Number of Anestesia Machines',
    ],
    'numanesthesiaconvert': [
        'Ventilator Counts-Ventilators Number of Anesthesia Machines that are converted to be used as a Vent',
        'Ventilator Counts-Ventilators Number of Anestesia Machines that are converted to be used as a Vent',
    ],
    'numcvd19onvent': [
        'Ventilator Usage-Ventilators Number of ventilators used for COVID-19 patients (confirmed)',
    ],
    'numecmo': [
        'Ventilator Usage-Ventilators ECMO units',
    ],
    'numecmouse': [
        'Ventilator Usage-Ventilators ECMO units in use',
    ],
    'numecmocvd19': [
        'Ventilator Usage-Ventilators ECMO units in use for COVID-19 patients',
    ],
    'aiiedtotal': [
        'Airborne Isolation Rooms-ED Total',
    ],
    'aiiedavailable': [
        'Airborne Isolation Rooms-ED Available',
    ],
    'aiiedoccupied': [
        'Airborne Isolation Rooms-ED Occupied requiring airborne isolation',
    ],
    'aiiedoccupiedcvd19': [
        'Airborne Isolation Rooms-ED Occupied by COVID-19 patient',
    ],
    'aiinonicutotal': [
        'Airborne Isolation Rooms-Inpatient non-ICU Total',
    ],
    'aiinonicuavail': [
        'Airborne Isolation Rooms-Inpatient non-ICU Available',
    ],
    'aiinonicuoccupied': [
        'Airborne Isolation Rooms-Inpatient non-ICU Occupied requiring airborne isolation',
    ],
    'aiinonicuoccupiedcvd19': [
        'Airborne Isolation Rooms-Inpatient non-ICU Occupied by COVID-19 patient',
    ],
    'aiiicutotal': [
        'Airborne Isolation Rooms-ICU Total',
    ],
    'aiiicuavail': [
        'Airborne Isolation Rooms-ICU Available',
    ],
    'aiiicuoccupied': [
        'Airborne Isolation Rooms-ICU Occupied requiring airborne isolation',
    ],
    'aiiicuoccupiedcvd19': [
        'Airborne Isolation Rooms-ICU Occupied by COVID-19 patient',
    ]
}

# this should be deprecated and removed in favor of using HeaderMapping
# which will load the contents of hos_mapping
short_long_column_header_map_HOS = {
    'aii24h': 'Other Beds-Airborne Infection Isolation 24hr Beds',
    'aii72h': 'Other Beds-Airborne Infection Isolation 72hr Beds',
    'aiiavail': 'Other Beds-Airborne Infection Isolation Current Available',
    'aiiedavailable': 'Airborne Isolation Rooms-ED Available',
    'aiiedoccupied': 'Airborne Isolation Rooms-ED Occupied requiring airborne isolation',
    'aiiedoccupiedcvd19': 'Airborne Isolation Rooms-ED Occupied by COVID-19 patient',
    'aiiedtotal': 'Airborne Isolation Rooms-ED Total',
    'aiiicuavail': 'Airborne Isolation Rooms-ICU Available',
    'aiiicuoccupied': 'Airborne Isolation Rooms-ICU Occupied requiring airborne isolation',
    'aiiicuoccupiedcvd19': 'Airborne Isolation Rooms-ICU Occupied by COVID-19 patient',
    'aiiicutotal': 'Airborne Isolation Rooms-ICU Total',
    'aiinonicuavail': 'Airborne Isolation Rooms-Inpatient non-ICU Available',
    'aiinonicuoccupied': 'Airborne Isolation Rooms-Inpatient non-ICU Occupied requiring airborne isolation',
    'aiinonicuoccupiedcvd19': 'Airborne Isolation Rooms-Inpatient non-ICU Occupied by COVID-19 patient',
    'aiinonicutotal': 'Airborne Isolation Rooms-Inpatient non-ICU Total',
    'aiistaff': 'Other Beds-Airborne Infection Isolation Staffed Beds',
    'burn24h': 'Available Beds-Burn 24hr Beds',
    'burn72h': 'Available Beds-Burn 72hr Beds',
    'burnavail': 'Available Beds-Burn Current Available',
    'burneyepro': 'Current Burn Rates per day for the following PPE (Single Units):-Eye Protection (Goggles Face shield) Response ?',
    'burngowns': 'Current Burn Rates per day for the following PPE (Single Units):-Gowns Response ?',
    'burnmask': 'Current Burn Rates per day for the following PPE (Single Units):-Facial Masks (Procedural/Surgical) Response ?',
    'burnn95': "Current Burn Rates per day for the following PPE (Single Units):-N95's Response ?",
    'burnpapr': "Current Burn Rates per day for the following PPE (Single Units):-PAPR's Response ?",
    'burnpaprfilter': "Current Burn Rates per day for the following PPE (Single Units):-PAPR's Filters Response ?",
    'burnpaprhoods': "Current Burn Rates per day for the following PPE (Single Units):-PAPR's Hoods Response ?",
    'burnstaff': 'Available Beds-Burn Staffed Beds',
    'consppecohortwdestaff': 'Are you currently implementing conservation strategies to preserve PPE:-Cohorting patients with dedicated staff Response ?',
    'consppecohortwodestaff': 'Are you currently implementing conservation strategies to preserve PPE:-Cohorting patients without dedicated staff Response ?',
    'consppedispon95': 'Are you currently implementing conservation strategies to preserve PPE:-Reuse of disposable N95 respirators Response ?',
    'conspperesp': 'Are you currently implementing conservation strategies to preserve PPE:-Extended use of respirators Response ?',
    'consppereuseresp': 'Are you currently implementing conservation strategies to preserve PPE:-Use of reusable respirators in place of disposable N95s (i.e. PAPRs elastomeric N95s etc.) Response ?',
    'consppestaffhours': 'Are you currently implementing conservation strategies to preserve PPE:-Extended staff hours/shifts Response ?',
    'cvd19pntadmitnonvent': 'Admission Data-Number of Patients awaiting admission with Confirmed or PUI COVID-19 non-ventilated Response ?',
    'cvd19pntadmitnvent': 'Admission Data-Number of Patients awaiting admission for Confirmed or PUI COVID-19 on ventilator Response ?',
    'cvd19tstpostve': 'How many of those inhouse tests were positive? ',
    'cvd19tstrun': 'How many COVID-19 tests were run at your inhouse lab today? ',
    'cvdnumc19died': 'COVID-19 Patient Counts-Number of patient deaths with Confirmed or PUI for COVID-19 in last 24 hours: ',
    'cvdnumc19hopats': 'COVID-19 Patient Counts-Total number of inpatients admitted 14+ days for other conditions now PUI or confirmed COVID-19?: ',
    'date': 'Local Testing-Real or future go-live date: ',
    'eddeceased': 'Emergency Department-ED Available Capacity Deceased',
    'eddelayed': 'Emergency Department-ED Available Capacity Delayed',
    'edimmediate': 'Emergency Department-ED Available Capacity Immediate',
    'edminor': 'Emergency Department-ED Available Capacity Minor',
    'envrnmntlsrvcsday': 'Todays Critical Staffing Shortages - Environmental Services',
    'envrnmntlsrvcsweek': 'Forecasted Critical Staffing Shortages - Environmental Services',
    'facrespplan': 'EEIs-Does your facility have an established respiratory protection plan? Response ?',
    'hospitalcity': 'HospitalCity',
    'hospitallatitude': 'HospitalLatitude',
    'hospitallongitude': 'HospitalLongitude',
    'hospitalname': 'HospitalName',
    'hospitalstate': 'HospitalState',
    'hospitalstreetaddress': 'HospitalStreetAddress',
    'hospitalzip': 'HospitalZip',
    'icu24h': 'Available Beds-Adult Intensive Care Unit (ICU) 24hr Beds',
    'icu72h': 'Available Beds-Adult Intensive Care Unit (ICU) 72hr Beds',
    'icuavail': 'Available Beds-Adult Intensive Care Unit (ICU) Current Available',
    'labordeliv24h': 'Other Beds-Labor / Delivery 24hr Beds',
    'labordeliv72h': 'Other Beds-Labor / Delivery 72hr Beds',
    'labordelivavail': 'Other Beds-Labor / Delivery Current Available',
    'labordelivstaff': 'Other Beds-Labor / Delivery Staffed Beds',
    'maternity24h': 'Other Beds-Maternity / Newborn Nursery 24hr Beds',
    'maternity72h': 'Other Beds-Maternity / Newborn Nursery 72hr Beds',
    'maternityavail': 'Other Beds-Maternity / Newborn Nursery Current Available',
    'maternitystaff': 'Other Beds-Maternity / Newborn Nursery Staffed Beds',
    'medsurg24h': 'Available Beds-Medical and Surgical (Med/Surg) 24hr Beds',
    'medsurg72h': 'Available Beds-Medical and Surgical (Med/Surg) 72hr Beds',
    'medsurgavail': 'Available Beds-Medical and Surgical (Med/Surg) Current Available',
    'medsurgstaff': 'Available Beds-Medical and Surgical (Med/Surg) Staffed Beds',
    'modelsfittested': 'EEIs-What mask brands and models are staff fit tested to use? Response ?',
    'n95fittested': 'EEIs-Is your facility planning to use N95 masks. If so is your staff fit-tested to wear N95 masks? Response ?',
    'n95util1528': 'At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-15-28 days Response ?',
    'n95util29more': 'At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-29 or more days Response ?',
    'n95util814': 'At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-8-14 days Response ?',
    'n95utli3less': 'At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-3 or less days Response ?',
    'n95utli47': 'At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-4-7 days Response ?',
    'needcleaning': 'Does your facility anticipate material/supply shortages of the following?-Cleaning/Disinfection Supplies Response ?',
    'needeyepro': 'Does your facility anticipate material/supply shortages of the following?-Eye Protection (Goggles Face shield) Response ?',
    'needgloves': 'Is there an immediate need for hand hygiene/disinfection supplies listed below?-Gloves Response ?',
    'needgown': 'Does your facility anticipate material/supply shortages of the following?-Gown/Apron Response ?',
    'needhandsoap': 'Is there an immediate need for hand hygiene/disinfection supplies listed below?-Hand Soap Response ?',
    'needmasks': 'Does your facility anticipate material/supply shortages of the following?-Facial Masks (Procedural/Surgical) Response ?',
    'needn95': "Does your facility anticipate material/supply shortages of the following?-N95's Response ?",
    'needother1': 'Is there an immediate need for hand hygiene/disinfection supplies listed below?-Other (please specify) Response ?',
    'needother2': 'Does your facility anticipate material/supply shortages of the following?-Other (please specify) Response ?',
    'needpapr': "Does your facility anticipate material/supply shortages of the following?-PAPR's Response ?",
    'needpaprfilters': "Does your facility anticipate material/supply shortages of the following?-PAPR's Filters Response ?",
    'needpaprhoods': "Does your facility anticipate material/supply shortages of the following?-PAPR's Hoods Response ?",
    'needsanitizer': 'Is there an immediate need for hand hygiene/disinfection supplies listed below?-Alcohol Based Hand Sanitizer Response ?',
    'needsolution': 'Is there an immediate need for hand hygiene/disinfection supplies listed below?-Disinfection Solutions Response ?',
    'needwipes': 'Is there an immediate need for hand hygiene/disinfection supplies listed below?-Disinfection Wipes Response ?',
    'nicu24h': 'Available Beds-Neonatal 24hr Beds',
    'nicu72h': 'Available Beds-Neonatal 72hr Beds',
    'nicuavail': 'Available Beds-Neonatal Current Available',
    'nicustaff': 'Available Beds-Neonatal Staffed Beds',
    'noncvd19pntadmit': 'Admission Data-Number of Patients awaiting admission Non COVID-19 Response ?',
    'nputil1528': 'At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-15-28 days Response ?',
    'nputil29more': 'At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-29 or more days Response ?',
    'nputil814': 'At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-8-14 days Response ?',
    'nputli3less': 'At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-3 or less days Response ?',
    'nputli47': 'At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-4-7 days Response ?',
    'numanesthesia': 'Ventilator Counts-Ventilators Number of Anesthesia Machines',
    'numanesthesiaconvert': 'Ventilator Counts-Ventilators Number of Anesthesia Machines that are converted to be used as a Vent',
    'numc19hosppats': 'COVID-19 Patient Counts-Total number of inpatients diagnosed with COVID-19: ',
    'numc19mechventpats': 'COVID-19 Patient Counts-Total number of inpatients diagnosed with COVID-19 on ventilators: ',
    'numcvd19onvent': 'Ventilator Usage-Ventilators Number of ventilators used for COVID-19 patients (confirmed)',
    'numecmo': 'Ventilator Usage-Ventilators ECMO units',
    'numecmocvd19': 'Ventilator Usage-Ventilators ECMO units in use for COVID-19 patients',
    'numecmouse': 'Ventilator Usage-Ventilators ECMO units in use',
    'numicubeds': 'Available Beds-Adult Intensive Care Unit (ICU) Staffed Beds',
    'numvent': 'Ventilator Counts-Ventilators Number of ventilators',
    'numventuse': 'Ventilator Counts-Ventilators Number of ventilators in use',
    'otherhcpday': 'Todays Critical Staffing Shortages -Other HCP Personnel (Other persons who work in the facilities not detailed above',
    'otherhcpdaylist': 'Todays Critical Staffing Shortages -What other HCP Personnel not listed above do you have a critical staff shortage of? ',
    'otherhcpweek': 'Forecasted Critical Staffing Shortages -Other HCP Personnel (Other persons who work in the facilities not detailed above',
    'otherhcpweeklist': 'Forecasted Critical Staffing Shortages -What other HCP Personnel not listed above do you have a critical staff shortage of? ',
    'otherindpendtday': 'Todays Critical Staffing Shortages -Other licensed independent practitioners: Advanced Practice Nurses, Physician Assistances',
    'otherindpendtweek': 'Forecasted Critical Staffing Shortages -Other licensed independent practitioners: Advanced Practice Nurses, Physician Assistances',
    'paprtrained': 'EEIs-Is your facility planning to use PAPRs. If so is your staff trained to use PAPRs? Response ?',
    'ped24h': 'Available Beds-Pediatric 24hr Beds',
    'ped72h': 'Available Beds-Pediatric 72hr Beds',
    'pedavail': 'Available Beds-Pediatric Current Available',
    'pedstaff': 'Available Beds-Pediatric Staffed Beds',
    'phtmcstday': 'Todays Critical Staffing Shortages -Pharmacists and Pharmacy Techs',
    'phtmcstweek': 'Forecasted Critical Staffing Shortages -Pharmacists and Pharmacy Techs',
    'physcnstday': 'Todays Critical Staffing Shortages -Physicans: Attending, Fellows',
    'physcnstweek': 'Forecasted Critical Staffing Shortages -Physicans: Attending, Fellows',
    'pic24h': 'Available Beds-Pediatric Intensive Care 24hr Beds',
    'pic72h': 'Available Beds-Pediatric Intensive Care 72hr Beds',
    'picavail': 'Available Beds-Pediatric Intensive Care Current Available',
    'picstaff': 'Available Beds-Pediatric Intensive Care Staffed Beds',
    'pntadmiticu': 'Admission Data-Number of Patients awaiting ICU Bed Response ?',
    'pntdischrg': 'Admission Data-Number of Patients awaiting discharge placement Response ?',
    'ppedondoff': 'EEIs-Is your staff adequately trained in correctly donning and doffing of PPE? Response ?',
    'ppeutil1528': 'At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-15-28 days Response ?',
    'ppeutil29more': 'At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-29 or more days Response ?',
    'ppeutil814': 'At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-8-14 days Response ?',
    'ppeutli3less': 'At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-3 or less days Response ?',
    'ppeutli47': 'At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-4-7 days Response ?',
    'psych24h': 'Psych Beds-Psychiatric 24hr Beds',
    'psych72h': 'Psych Beds-Psychiatric 72hr Beds',
    'psychadol24h': 'Psych Beds-Adolescent 24hr Beds',
    'psychadol72h': 'Psych Beds-Adolescent 72hr Beds',
    'psychadolavail': 'Psych Beds-Adolescent Current Available',
    'psychadolstaff': 'Psych Beds-Adolescent Staffed Beds',
    'psychadult24h': 'Psych Beds-Adult 24hr Beds',
    'psychadult72h': 'Psych Beds-Adult 72hr Beds',
    'psychadultavail': 'Psych Beds-Adult Current Available',
    'psychadultstaff': 'Psych Beds-Adult Staffed Beds',
    'psychavail': 'Psych Beds-Psychiatric Current Available',
    'psychgeri24h': 'Psych Beds-Geriatric 24hr Beds',
    'psychgeri72h': 'Psych Beds-Geriatric 72hr Beds',
    'psychgeriavail': 'Psych Beds-Geriatric Current Available',
    'psychgeristaff': 'Psych Beds-Geriatric Staffed Beds',
    'psychmeddetox24h': 'Psych Beds-Medical Detox 24hr Beds',
    'psychmeddetox72h': 'Psych Beds-Medical Detox 72hr Beds',
    'psychmeddetoxavail': 'Psych Beds-Medical Detox Current Available',
    'psychmeddetoxstaff': 'Psych Beds-Medical Detox Staffed Beds',
    'psychsadd24h': 'Psych Beds-Substance Abuse (Dual Diagnosis) 24hr Beds',
    'psychsadd72h': 'Psych Beds-Substance Abuse (Dual Diagnosis) 72hr Beds',
    'psychsaddavail': 'Psych Beds-Substance Abuse (Dual Diagnosis) Current Available',
    'psychsaddstaff': 'Psych Beds-Substance Abuse (Dual Diagnosis) Staffed Beds',
    'psychstaff': 'Psych Beds-Psychiatric Staffed Beds',
    'rehab24h': 'Available Beds-Inpatient Rehab 24hr Beds',
    'rehab72h': 'Available Beds-Inpatient Rehab 72hr Beds',
    'rehabavail': 'Available Beds-Inpatient Rehab Current Available',
    'rehabstaff': 'Available Beds-Inpatient Rehab Staffed Beds',
    'rnlpnday': 'Todays Critical Staffing Shortages -Nurses: RN and LPNs',
    'rnlpnweek': 'Forecasted Critical Staffing Shortages -Nurses: RN and LPNs',
    'rsprtrythrpstday': 'Todays Critical Staffing Shortages -Respritory Therapists',
    'rsprtrythrpstweek': 'Forecasted Critical Staffing Shortages -Respritory Therapists',
    'shortcleaning': 'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Cleaning/Disinfection Supplies Response ?',
    'shortcollection': 'Testing Supplies-What diagnostic testing or specimen collection supplies do you anticipate a shortage of? ',
    'shorteyepro': 'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Eye Protection (Goggles Face shield) Response ?',
    'shortgowns': 'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Gowns Response ?',
    'shortmasks': 'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Facial Masks (Procedural/Surgical) Response ?',
    'shortn95': "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-N95's Response ?",
    'shortother1': 'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Other (please specify) Response ?',
    'shortother2': 'Testing Supplies-Other (please specify) ',
    'shortpapr': "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-PAPR's Response ?",
    'shortpaprfilters': "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-PAPR's Filters Response ?",
    'shortpaprhoods': "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-PAPR's Hoods Response ?",
    'shortsanitizer': 'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Hand Sanitizer Response ?',
    'shortsoap': 'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Hand Soap Response ?',
    'tempday': 'Todays Critical Staffing Shortages -Temporary physicians, nurse, etc (per diems, travelers, retired, seasonal)',
    'tempweek': 'Forecasted Critical Staffing Shortages -Temporary physicians, nurse, etc (per diems, travelers, retired, seasonal)',
    'testlocal': 'Local Testing-Do you have a commercial or inhouse platform for performing local testing of COVID-19? ',
    'ttlaiied': 'COVID-19 Patient Counts-How many airborne infection isolation rooms are in your ED? ',
    'ttlaiiicu': 'COVID-19 Patient Counts-How many airborne infection isolation rooms are in your ICU? ',
    'ttlaiinonicu': 'COVID-19 Patient Counts-How many airborne infection isolation rooms are in non-ICU? ',
    'ttlcalloutchildcare': 'Employee Status-Call out reason: child care issues ',
    'ttlcalloutisolation': 'Employee Status-Call out reason: quarantine or isolation due to exposure ',
    'ttlcalloutnurse': 'Employee Status-Number of Call Outs that are Nurses ',
    'ttlcalloutphys': 'Employee Status-Number of Call Outs that are Physicians ',
    'ttlcvd19ptntecmo': 'COVID-19 Patient Counts-Total number of inpatients diagnosed with COVID-19 on ECMO: ',
    'ttlcvd19pui': 'COVID-19 Patient Counts-Total number of inpatients under suspicion for COVID-19 (PUI): ',
    'ttlempcall': 'Employee Status-Total Employee Call Outs/Absenteeism ',
    'ttlempcvd19': 'Employee Status-Call out reason: sick with COVID-19 ',
    'ttlnumicubedscvd19': 'COVID-19 Patient Counts - Total number of ICU beds occupied by a diagnosed COVID-19 patient:'
}

# this should be deprecated and removed in favor of using HeaderMapping
# which will load the contents of hos_mapping
long_short_column_header_map_HOS = {
    "HospitalName": "hospitalname",
    "HospitalStreetAddress": "hospitalstreetaddress",
    "HospitalCity": "hospitalcity",
    "HospitalState": "hospitalstate",
    "HospitalZip": "hospitalzip",
    "HospitalLatitude": "hospitallatitude",
    "HospitalLongitude": "hospitallongitude",
    "Available Beds-Adult Intensive Care Unit (ICU) Staffed Beds": "numicubeds",
    "Available Beds-Adult Intensive Care Unit (ICU) Current Available": "icuavail",
    "Available Beds-Adult Intensive Care Unit (ICU) 24hr Beds": "icu24h",
    "Available Beds-Adult Intensive Care Unit (ICU) 72hr Beds": "icu72h",
    "Available Beds-Medical and Surgical (Med/Surg) Staffed Beds": "medsurgstaff",
    "Available Beds-Medical and Surgical (Med/Surg) Current Available": "medsurgavail",
    "Available Beds-Medical and Surgical (Med/Surg) 24hr Beds": "medsurg24h",
    "Available Beds-Medical and Surgical (Med/Surg) 72hr Beds": "medsurg72h",
    "Available Beds-Burn Staffed Beds": "burnstaff",
    "Available Beds-Burn Current Available": "burnavail",
    "Available Beds-Burn 24hr Beds": "burn24h",
    "Available Beds-Burn 72hr Beds": "burn72h",
    "Available Beds-Pediatric Intensive Care Staffed Beds": "picstaff",
    "Available Beds-Pediatric Intensive Care Current Available": "picavail",
    "Available Beds-Pediatric Intensive Care 24hr Beds": "pic24h",
    "Available Beds-Pediatric Intensive Care 72hr Beds": "pic72h",
    "Available Beds-Pediatric Staffed Beds": "pedstaff",
    "Available Beds-Pediatric Current Available": "pedavail",
    "Available Beds-Pediatric 24hr Beds": "ped24h",
    "Available Beds-Pediatric 72hr Beds": "ped72h",
    "Available Beds-Neonatal Staffed Beds": "nicustaff",
    "Available Beds-Neonatal Current Available": "nicuavail",
    "Available Beds-Neonatal 24hr Beds": "nicu24h",
    "Available Beds-Neonatal 72hr Beds": "nicu72h",
    "Available Beds-Inpatient Rehab Staffed Beds": "rehabstaff",
    "Available Beds-Inpatient Rehab Current Available": "rehabavail",
    "Available Beds-Inpatient Rehab 24hr Beds": "rehab24h",
    "Available Beds-Inpatient Rehab 72hr Beds": "rehab72h",
    "Psych Beds-Psychiatric Staffed Beds": "psychstaff",
    "Psych Beds-Psychiatric Current Available": "psychavail",
    "Psych Beds-Psychiatric 24hr Beds": "psych24h",
    "Psych Beds-Psychiatric 72hr Beds": "psych72h",
    "Psych Beds-Adult Staffed Beds": "psychadultstaff",
    "Psych Beds-Adult Current Available": "psychadultavail",
    "Psych Beds-Adult 24hr Beds": "psychadult24h",
    "Psych Beds-Adult 72hr Beds": "psychadult72h",
    "Psych Beds-Adolescent Staffed Beds": "psychadolstaff",
    "Psych Beds-Adolescent Current Available": "psychadolavail",
    "Psych Beds-Adolescent 24hr Beds": "psychadol24h",
    "Psych Beds-Adolescent 72hr Beds": "psychadol72h",
    "Psych Beds-Geriatric Staffed Beds": "psychgeristaff",
    "Psych Beds-Geriatric Current Available": "psychgeriavail",
    "Psych Beds-Geriatric 24hr Beds": "psychgeri24h",
    "Psych Beds-Geriatric 72hr Beds": "psychgeri72h",
    "Psych Beds-Medical Detox Staffed Beds": "psychmeddetoxstaff",
    "Psych Beds-Medical Detox Current Available": "psychmeddetoxavail",
    "Psych Beds-Medical Detox 24hr Beds": "psychmeddetox24h",
    "Psych Beds-Medical Detox 72hr Beds": "psychmeddetox72h",
    "Psych Beds-Substance Abuse (Dual Diagnosis) Staffed Beds": "psychsaddstaff",
    "Psych Beds-Substance Abuse (Dual Diagnosis) Current Available": "psychsaddavail",
    "Psych Beds-Substance Abuse (Dual Diagnosis) 24hr Beds": "psychsadd24h",
    "Psych Beds-Substance Abuse (Dual Diagnosis) 72hr Beds": "psychsadd72h",
    "Other Beds-Labor / Delivery Staffed Beds": "labordelivstaff",
    "Other Beds-Labor / Delivery Current Available": "labordelivavail",
    "Other Beds-Labor / Delivery 24hr Beds": "labordeliv24h",
    "Other Beds-Labor / Delivery 72hr Beds": "labordeliv72h",
    "Other Beds-Maternity / Newborn Nursery Staffed Beds": "maternitystaff",
    "Other Beds-Maternity / Newborn Nursery Current Available": "maternityavail",
    "Other Beds-Maternity / Newborn Nursery 24hr Beds": "maternity24h",
    "Other Beds-Maternity / Newborn Nursery 72hr Beds": "maternity72h",
    "Other Beds-Airborne Infection Isolation Staffed Beds": "aiistaff",
    "Other Beds-Airborne Infection Isolation Current Available": "aiiavail",
    "Other Beds-Airborne Infection Isolation 24hr Beds": "aii24h",
    "Other Beds-Airborne Infection Isolation 72hr Beds": "aii72h",
    "Emergency Department-ED Available Capacity Immediate": "edimmediate",
    "Emergency Department-ED Available Capacity Delayed": "eddelayed",
    "Emergency Department-ED Available Capacity Minor": "edminor",
    "Emergency Department-ED Available Capacity Deceased": "eddeceased",
    "Admission Data-Number of Patients awaiting admission Non COVID-19 Response ?": "noncvd19pntadmit",
    "Admission Data-Number of Patients awaiting admission with Confirmed or PUI COVID-19 non-ventilated Response ?": "cvd19pntadmitnonvent",
    "Admission Data-Number of Patients awaiting admission for Confirmed or PUI COVID-19 on ventilator Response ?": "cvd19pntadmitnvent",
    "Admission Data-Number of Patients awaiting ICU Bed Response ?": "pntadmiticu",
    "Admission Data-Number of Patients awaiting discharge placement Response ?": "pntdischrg",
    "EEIs-Does your facility have an established respiratory protection plan? Response ?": "facrespplan",
    "EEIs-Is your facility planning to use N95 masks. If so is your staff fit-tested to wear N95 masks? Response ?": "n95fittested",
    "EEIs-What mask brands and models are staff fit tested to use? Response ?": "modelsfittested",
    "EEIs-Is your facility planning to use PAPRs. If so is your staff trained to use PAPRs? Response ?": "paprtrained",
    "EEIs-Is your staff adequately trained in correctly donning and doffing of PPE? Response ?": "ppedondoff",
    "Is there an immediate need for hand hygiene/disinfection supplies listed below?-Alcohol Based Hand Sanitizer Response ?": "needsanitizer",
    "Is there an immediate need for hand hygiene/disinfection supplies listed below?-Hand Soap Response ?": "needhandsoap",
    "Is there an immediate need for hand hygiene/disinfection supplies listed below?-Disinfection Solutions Response ?": "needsolution",
    "Is there an immediate need for hand hygiene/disinfection supplies listed below?-Disinfection Wipes Response ?": "needwipes",
    "Is there an immediate need for hand hygiene/disinfection supplies listed below?-Gloves Response ?": "needgloves",
    "Is there an immediate need for hand hygiene/disinfection supplies listed below?-Other (please specify) Response ?": "needother1",
    "Does your facility anticipate material/supply shortages of the following?-N95's Response ?": "needn95",
    "Does your facility anticipate material/supply shortages of the following?-PAPR's Response ?": "needpapr",
    "Does your facility anticipate material/supply shortages of the following?-PAPR's Hoods Response ?": "needpaprhoods",
    "Does your facility anticipate material/supply shortages of the following?-PAPR's Filters Response ?": "needpaprfilters",
    "Does your facility anticipate material/supply shortages of the following?-Facial Masks (Procedural/Surgical) Response ?": "needmasks",
    "Does your facility anticipate material/supply shortages of the following?-Gown/Apron Response ?": "needgown",
    "Does your facility anticipate material/supply shortages of the following?-Eye Protection (Goggles Face shield) Response ?": "needeyepro",
    "Does your facility anticipate material/supply shortages of the following?-Cleaning/Disinfection Supplies Response ?": "needcleaning",
    "Does your facility anticipate material/supply shortages of the following?-Other (please specify) Response ?": "needother2",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-N95's Response ?": "shortn95",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-PAPR's Response ?": "shortpapr",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-PAPR's Hoods Response ?": "shortpaprhoods",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-PAPR's Filters Response ?": "shortpaprfilters",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Facial Masks (Procedural/Surgical) Response ?": "shortmasks",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Gowns Response ?": "shortgowns",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Eye Protection (Goggles Face shield) Response ?": "shorteyepro",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Hand Soap Response ?": "shortsoap",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Hand Sanitizer Response ?": "shortsanitizer",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Cleaning/Disinfection Supplies Response ?": "shortcleaning",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Other (please specify) Response ?": "shortother1",
    "Current Burn Rates per day for the following PPE (Single Units):-N95's Response ?": "burnn95",
    "Current Burn Rates per day for the following PPE (Single Units):-PAPR's Response ?": "burnpapr",
    "Current Burn Rates per day for the following PPE (Single Units):-PAPR's Hoods Response ?": "burnpaprhoods",
    "Current Burn Rates per day for the following PPE (Single Units):-PAPR's Filters Response ?": "burnpaprfilter",
    "Current Burn Rates per day for the following PPE (Single Units):-Facial Masks (Procedural/Surgical) Response ?": "burnmask",
    "Current Burn Rates per day for the following PPE (Single Units):-Gowns Response ?": "burngowns",
    "Current Burn Rates per day for the following PPE (Single Units):-Eye Protection (Goggles Face shield) Response ?": "burneyepro",
    "Testing Supplies-What diagnostic testing or specimen collection supplies do you anticipate a shortage of? ": "shortcollection",
    "Testing Supplies-Other (please specify) ": "shortother2",
    "Local Testing-Do you have a commercial or inhouse platform for performing local testing of COVID-19? ": "testlocal",
    "Local Testing-Real or future go-live date: ": "date",
    "How many COVID-19 tests were run at your inhouse lab today? ": "cvd19tstrun",
    "How many of those inhouse tests were positive? ": "cvd19tstpostve",
    "COVID-19 Patient Counts-Total number of inpatients diagnosed with COVID-19: ": "numc19hosppats",
    "COVID-19 Patient Counts-Total number of inpatients under suspicion for COVID-19 (PUI): ": "ttlcvd19pui",
    "COVID-19 Patient Counts - Total number of ICU beds occupied by a diagnosed COVID-19 patient:": "ttlnumicubedscvd19",
    "COVID-19 Patient Counts-Total number of inpatients admitted 14+ days for other conditions now PUI or confirmed COVID-19?: ": "cvdnumc19hopats",
    "COVID-19 Patient Counts-Total number of inpatients diagnosed with COVID-19 on ventilators: ": "numc19mechventpats",
    "COVID-19 Patient Counts-Total number of inpatients diagnosed with COVID-19 on ECMO: ": "ttlcvd19ptntecmo",
    "COVID-19 Patient Counts-How many airborne infection isolation rooms are in your ED? ": "ttlaiied",
    "COVID-19 Patient Counts-How many airborne infection isolation rooms are in your ICU? ": "ttlaiiicu",
    "COVID-19 Patient Counts-How many airborne infection isolation rooms are in non-ICU? ": "ttlaiinonicu",
    "COVID-19 Patient Counts-Number of patient deaths with Confirmed or PUI for COVID-19 in last 24 hours: ": "cvdnumc19died",
    "Are you currently implementing conservation strategies to preserve PPE:-Extended use of respirators Response ?": "conspperesp",
    "Are you currently implementing conservation strategies to preserve PPE:-Use of reusable respirators in place of disposable N95s (i.e. PAPRs elastomeric N95s etc.) Response ?": "consppereuseresp",
    "Are you currently implementing conservation strategies to preserve PPE:-Reuse of disposable N95 respirators Response ?": "consppedispon95",
    "Are you currently implementing conservation strategies to preserve PPE:-Extended staff hours/shifts Response ?": "consppestaffhours",
    "Are you currently implementing conservation strategies to preserve PPE:-Cohorting patients without dedicated staff Response ?": "consppecohortwodestaff",
    "Are you currently implementing conservation strategies to preserve PPE:-Cohorting patients with dedicated staff Response ?": "consppecohortwdestaff",
    "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-3 or less days Response ?": "n95utli3less",
    "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-4-7 days Response ?": "n95utli47",
    "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-8-14 days Response ?": "n95util814",
    "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-15-28 days Response ?": "n95util1528",
    "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-29 or more days Response ?": "n95util29more",
    "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-3 or less days Response ?": "ppeutli3less",
    "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-4-7 days Response ?": "ppeutli47",
    "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-8-14 days Response ?": "ppeutil814",
    "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-15-28 days Response ?": "ppeutil1528",
    "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-29 or more days Response ?": "ppeutil29more",
    "At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-3 or less days Response ?": "nputli3less",
    "At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-4-7 days Response ?": "nputli47",
    "At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-8-14 days Response ?": "nputil814",
    "At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-15-28 days Response ?": "nputil1528",
    "At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-29 or more days Response ?": "nputil29more",
    "Employee Status-Total Employee Call Outs/Absenteeism ": "ttlempcall",
    "Employee Status-Call out reason: sick with COVID-19 ": "ttlempcvd19",
    "Employee Status-Number of Call Outs that are Physicians ": "ttlcalloutphys",
    "Employee Status-Number of Call Outs that are Nurses ": "ttlcalloutnurse",
    "Employee Status-Call out reason: quarantine or isolation due to exposure ": "ttlcalloutisolation",
    "Employee Status-Call out reason: child care issues ": "ttlcalloutchildcare",
    "Todays Critical Staffing Shortages - Environmental Services": "envrnmntlsrvcsday",
    "Todays Critical Staffing Shortages -Nurses: RN and LPNs": "rnlpnday",
    "Todays Critical Staffing Shortages -Respritory Therapists": "rsprtrythrpstday",
    "Todays Critical Staffing Shortages -Pharmacists and Pharmacy Techs": "phtmcstday",
    "Todays Critical Staffing Shortages -Physicans: Attending, Fellows": "physcnstday",
    "Todays Critical Staffing Shortages -Other licensed independent practitioners: Advanced Practice Nurses, Physician Assistances": "otherindpendtday",
    "Todays Critical Staffing Shortages -Temporary physicians, nurse, etc (per diems, travelers, retired, seasonal)": "tempday",
    "Todays Critical Staffing Shortages -Other HCP Personnel (Other persons who work in the facilities not detailed above": "otherhcpday",
    "Todays Critical Staffing Shortages -What other HCP Personnel not listed above do you have a critical staff shortage of? ": "otherhcpdaylist",
    "Forecasted Critical Staffing Shortages - Environmental Services": "envrnmntlsrvcsweek",
    "Forecasted Critical Staffing Shortages -Nurses: RN and LPNs": "rnlpnweek",
    "Forecasted Critical Staffing Shortages -Respritory Therapists": "rsprtrythrpstweek",
    "Forecasted Critical Staffing Shortages -Pharmacists and Pharmacy Techs": "phtmcstweek",
    "Forecasted Critical Staffing Shortages -Physicans: Attending, Fellows": "physcnstweek",
    "Forecasted Critical Staffing Shortages -Other licensed independent practitioners: Advanced Practice Nurses, Physician Assistances": "otherindpendtweek",
    "Forecasted Critical Staffing Shortages -Temporary physicians, nurse, etc (per diems, travelers, retired, seasonal)": "tempweek",
    "Forecasted Critical Staffing Shortages -Other HCP Personnel (Other persons who work in the facilities not detailed above": "otherhcpweek",
    "Forecasted Critical Staffing Shortages -What other HCP Personnel not listed above do you have a critical staff shortage of? ": "otherhcpweeklist",
    "Ventilator Counts-Ventilators Number of ventilators": "numvent",
    "Ventilator Counts-Ventilators Number of ventilators in use": "numventuse",
    "Ventilator Counts-Ventilators Number of Anesthesia Machines": "numanesthesia",
    "Ventilator Counts-Ventilators Number of Anesthesia Machines that are converted to be used as a Vent": "numanesthesiaconvert",
    "Ventilator Usage-Ventilators Number of ventilators used for COVID-19 patients (confirmed)": "numcvd19onvent",
    "Ventilator Usage-Ventilators ECMO units": "numecmo",
    "Ventilator Usage-Ventilators ECMO units in use": "numecmouse",
    "Ventilator Usage-Ventilators ECMO units in use for COVID-19 patients": "numecmocvd19",
    "Airborne Isolation Rooms-ED Total": "aiiedtotal",
    "Airborne Isolation Rooms-ED Available": "aiiedavailable",
    "Airborne Isolation Rooms-ED Occupied requiring airborne isolation": "aiiedoccupied",
    "Airborne Isolation Rooms-ED Occupied by COVID-19 patient": "aiiedoccupiedcvd19",
    "Airborne Isolation Rooms-Inpatient non-ICU Total": "aiinonicutotal",
    "Airborne Isolation Rooms-Inpatient non-ICU Available": "aiinonicuavail",
    "Airborne Isolation Rooms-Inpatient non-ICU Occupied requiring airborne isolation": "aiinonicuoccupied",
    "Airborne Isolation Rooms-Inpatient non-ICU Occupied by COVID-19 patient": "aiinonicuoccupiedcvd19",
    "Airborne Isolation Rooms-ICU Total": "aiiicutotal",
    "Airborne Isolation Rooms-ICU Available": "aiiicuavail",
    "Airborne Isolation Rooms-ICU Occupied requiring airborne isolation": "aiiicuoccupied",
    "Airborne Isolation Rooms-ICU Occupied by COVID-19 patient": "aiiicuoccupiedcvd19",
}

# this will be used as the basis for ltc_mapping, which will be modeled
# after hos_mapping
long_short_column_header_map_LTC = {
    "LTCName": "LTCName",
    "LTCStreetAddress": "LTCStreetAddress",
    "LTCState": "LTCState",
    "LTCCity": "LTCCity",
    "LTCZip": "LTCZip",
    "LTCLatitude": "LTCLatitude",
    "LTCLongitude": "LTCLongitude",
    "Total Available-Beds Staffed Beds": "ttlavlbdsstffd",
    "Total Available-Beds Currently Available": "ttlavlbdsavl",
    "Gender-Male Staffed Beds": "mlstffdbds",
    "Gender-Male Currently Available": "mlavl",
    "Gender-Female Staffed Beds": "fmalstff",
    "Gender-Female Currently Available": "fmalavl",
    "Care Level / Approved Stay Status-Personal Care Staffed Beds": "prsnlcrstff",
    "Care Level / Approved Stay Status-Personal Care Currently Available": "prsnlcravl",
    "Care Level / Approved Stay Status-Assisted Living Staffed Beds": "asstdlvngstff",
    "Care Level / Approved Stay Status-Assisted Living Currently Available": "asstdlvngavl",
    "Care Level / Approved Stay Status-Skilled Nursing Care Staffed Beds": "skllnrsstff",
    "Care Level / Approved Stay Status-Skilled Nursing Care Currently Available": "skllnrsavl",
    "Care Level / Approved Stay Status-Rehab Staffed Beds": "rhbstff",
    "Care Level / Approved Stay Status-Rehab Currently Available": "rhbavl",
    "Care Level / Approved Stay Status-Continuing Care Staffed Beds": "cntcrstff",
    "Care Level / Approved Stay Status-Continuing Care Currently Available": "cntcravl",
    "Insurance-Medicare Staffed Beds": "mdcrstff",
    "Insurance-Medicare Currently Available": "mdcravl",
    "Insurance-Medicaid Staffed Beds": "mdcdstff",
    "Insurance-Medicaid Currently Available": "mdcdavl",
    "Insurance-Private Staffed Beds": "prvtstff",
    "Insurance-Private Currently Available": "prvtavl",
    "Insurance-Personal Resource (Self-Pay) Staffed Beds": "slfpystff",
    "Insurance-Personal Resource (Self-Pay) Currently Available": "slfpyavl",
    "Insurance-Other Staffed Beds": "othrstff",
    "Insurance-Other Currently Available": "othravl",
    "Technology / Care Considerations-Tracheotomy Staffed Beds": "trchtmystff",
    "Technology / Care Considerations-Tracheotomy Currently Available": "trchtmyavl",
    "Technology / Care Considerations-Ventilator Staffed Beds": "vntltrstff",
    "Technology / Care Considerations-Ventilator Currently Available": "vntltravl",
    "Technology / Care Considerations-CPAP Staffed Beds": "cpapstff",
    "Technology / Care Considerations-CPAP Currently Available": "cpapavl",
    "Technology / Care Considerations-Feeding Tube Staffed Beds": "fdgtbstff",
    "Technology / Care Considerations-Feeding Tube Currently Available": "fdgtbavl",
    "Technology / Care Considerations-Isolation Staffed Beds": "isostff",
    "Technology / Care Considerations-Isolation Currently Available": "isoavl",
    "Technology / Care Considerations-Cardiac Monitoring Staffed Beds": "cdcmntrstff",
    "Technology / Care Considerations-Cardiac Monitoring Currently Available": "cdcmntavl",
    "Technology / Care Considerations-IV Therapy Staffed Beds": "ivthrpystff",
    "Technology / Care Considerations-IV Therapy Currently Available": "ivthrpyavl",
    "Special Needs-Bariatric Staffed Beds": "brtrcstff",
    "Special Needs-Bariatric Currently Available": "brtravl",
    "Special Needs-Memory Care / Secured Staffed Beds": "mmrystff",
    "Special Needs-Memory Care / Secured Currently Available": "mmryavl",
    "Special Needs-Dialysis Staffed Beds": "dlysatff",
    "Special Needs-Dialysis Currently Available": "dlysavl",
    "Special Needs-Forensic Court Impairment Staffed Beds": "frnscimprstff",
    "Special Needs-Forensic Court Impairment Currently Available": "frnscimpravl",
    "Special Needs-Smoker Staffed Beds": "smkrstff",
    "Special Needs-Smoker Currently Available": "smkravl",
    "Special Needs-Wanderer Staffed Beds": "wndrstff",
    "Special Needs-Wanderer Currently Available": "wndravl",
    "Admission Data-Number of New Patients awaiting admission Response ?": "numnwptnt",
    "Admission Data-Number of single occupancy rooms available for COVID-19 Patients Response ?": "numcvd19rms",
    "Admission Data-Number of Residents on Hospice Response ?": "numreshspc",
    "Admission Data-Number of Residents with DNR Status Response ?": "numresdnr",
    "Admission Data-Number of Residents on Sex Offender List Response ?": "numressxoffndr",
    "Admission Data-Number of Residents in Isolation for NON-COVID Reasons Response ?": "numresisoncvd19",
    "Admission Data-Number of Residents that would require an ambulance to transfer Response ?": "numresambu",
    "EEIs-Does your facility have an established respiratory protection plan? Response ?": "facrespplan",
    "EEIs-Is your facility planning to use N95 masks. If so is your staff fit-tested to wear N95 masks? Response ?": "n95fittested",
    "EEIs-What mask brands and models are staff fit tested to use? Response ?": "modelsfittested",
    "EEIs-Is your facility planning to use PAPRs. If so is your staff trained to use PAPRs? Response ?": "paprtrained",
    "EEIs-Is your staff adequately trained in correctly donning and doffing of PPE? Response ?": "ppedondoff",
    "Is there an immediate need for hand hygiene/disinfection supplies listed below?-Alcohol Based Hand Sanitizer Response ?": "needsanitizer",
    "Is there an immediate need for hand hygiene/disinfection supplies listed below?-Hand Soap Response ?": "needhandsoap",
    "Is there an immediate need for hand hygiene/disinfection supplies listed below?-Disinfection Solutions Response ?": "needsolution",
    "Is there an immediate need for hand hygiene/disinfection supplies listed below?-Disinfection Wipes Response ?": "needwipes",
    "Is there an immediate need for hand hygiene/disinfection supplies listed below?-Gloves Response ?": "needgloves",
    "Is there an immediate need for hand hygiene/disinfection supplies listed below?-Other (please specify) Response ?": "needother1",
    "Does your facility anticipate material/supply shortages of the following?-N95's Response ?": "needn95",
    "Does your facility anticipate material/supply shortages of the following?-PAPR's Response ?": "needpapr",
    "Does your facility anticipate material/supply shortages of the following?-PAPR's Hoods Response ?": "needpaprhoods",
    "Does your facility anticipate material/supply shortages of the following?-PAPR's Filters Response ?": "needpaprfilters",
    "Does your facility anticipate material/supply shortages of the following?-Facial Masks (Procedural/Surgical) Response ?": "needmasks",
    "Does your facility anticipate material/supply shortages of the following?-Gown/Apron Response ?": "needgown",
    "Does your facility anticipate material/supply shortages of the following?-Eye Protection (Goggles Face shield) Response ?": "needeyepro",
    "Does your facility anticipate material/supply shortages of the following?-Cleaning/Disinfection Supplies Response ?": "needcleaning",
    "Does your facility anticipate material/supply shortages of the following?-Other (please specify) Response ?": "needother2",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-N95's Response ?": "shortn95",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-PAPR's Response ?": "shortpapr",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-PAPR's Hoods Response ?": "shortpaprhoods",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-PAPR's Filters Response ?": "shortpaprfilters",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Facial Masks (Procedural/Surgical) Response ?": "shortmasks",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Gowns Response ?": "shortgowns",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Eye Protection (Goggles Face shield) Response ?": "shorteyepro",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Hand Soap Response ?": "shortsoap",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Hand Sanitizer Response ?": "shortsanitizer",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Cleaning/Disinfection Supplies Response ?": "shortcleaning",
    "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Other (please specify) Response ?": "shortother1",
    "Current Burn Rates per day for the following PPE (Single Units):-N95's Response ?": "burnn95",
    "Current Burn Rates per day for the following PPE (Single Units):-PAPR's Response ?": "burnpapr",
    "Current Burn Rates per day for the following PPE (Single Units):-PAPR's Hoods Response ?": "burnpaprhoods",
    "Current Burn Rates per day for the following PPE (Single Units):-PAPR's Filters Response ?": "burnpaprfilter",
    "Current Burn Rates per day for the following PPE (Single Units):-Facial Masks (Procedural/Surgical) Response ?": "burnmask",
    "Current Burn Rates per day for the following PPE (Single Units):-Gowns Response ?": "burngowns",
    "Current Burn Rates per day for the following PPE (Single Units):-Eye Protection (Goggles Face shield) Response ?": "burneyepro",
    "COVID-19 Resident Counts-Total number of Residents diagnosed with COVID-19: ": "ttlreswcvd19",
    "COVID-19 Resident Counts-Total number of Residents under suspicion for COVID-19 (PUI): ": "ttlrespuicvd19",
    "Are you currently implementing conservation strategies to preserve PPE:-Extended use of respirators Response ?": "conspperesp",
    "Are you currently implementing conservation strategies to preserve PPE:-Use of reusable respirators in place of disposable N95s (i.e. PAPRs elastomeric N95s etc.) Response ?": "consppereuseresp",
    "Are you currently implementing conservation strategies to preserve PPE:-Reuse of disposable N95 respirators Response ?": "consppedispon95",
    "Are you currently implementing conservation strategies to preserve PPE:-Extended staff hours/shifts Response ?": "consppestaffhours",
    "Are you currently implementing conservation strategies to preserve PPE:-Cohorting Residents without dedicated staff Response ?": "consppecohortwodestaff",
    "Are you currently implementing conservation strategies to preserve PPE:-Cohorting Residents with dedicated staff Response ?": "consppecohortwdestaff",
    "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-3 or less days Response ?": "n95utli3less",
    "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-4-7 days Response ?": "n95utli47",
    "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-8-14 days Response ?": "n95util814",
    "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-15-28 days Response ?": "n95util1528",
    "At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-29 or more days Response ?": "n95util29more",
    "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-3 or less days Response ?": "ppeutli3less",
    "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-4-7 days Response ?": "ppeutli47",
    "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-8-14 days Response ?": "ppeutil814",
    "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-15-28 days Response ?": "ppeutil1528",
    "At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-29 or more days Response ?": "ppeutil29more",
    "Employee Status-Total Employee Call Outs/Absenteeism ": "ttlempcall",
    "Employee Status-Number of Call Outs that are RN ": "numcorn",
    "Employee Status-Number of Call Outs that are LPN/CNA ": "numcolpncna",
    "Employee Status-Number of Call Outs that are Personal Care Assistants ": "numcopca",
    "Employee Status-Call out reason: sick with COVID-19 ": "ttlempcvd19",
    "Employee Status-Call out reason: quarantine or isolation due to exposure ": "ttlcalloutisolation",
    "Employee Status-Call out reason: child care issues ": "ttlcalloutchildcare",
}

county_sum_columns = [
    "HospitalCounty",
    'icuavail',
    'numicubeds',
    'medsurgavail',
    'medsurgstaff',
    'picavail',
    'picstaff',
    'pedavail',
    'pedstaff',
    'aiiavail',
    'aiistaff',
    'numc19mechventpats',
    'ttlcvd19ptntecmo',
    'numc19hosppats',
    'numvent',
    'numventuse'
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
        "3": "n95utli3less",
        "7": "n95utli47",
        "14": "n95util814",
        "28":  "n95util1528",
        "29":  "n95util29more"
    },
    "PPE": {
        "3": "ppeutli3less",
        "7": "ppeutli47",
        "14": "ppeutil814",
        "28": "ppeutil1528",
        "29": "ppeutil29more"
    },
    "NP Specimen Collection Supplies": {
        "3": "nputli3less",
        "7": "nputli47",
        "14": "nputil814",
        "28": "nputil1528",
        "29": "nputil29more"
    }
}



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


# map bad/mispelled headers to the correct headers.
canonical_headers  = {
 'Admission Data-Number of Patients awaiting admission for Confirmed or PUI COVID 19 on ventilator Response ?': 'Admission Data-Number of Patients awaiting admission for Confirmed or PUI COVID-19 on ventilator Response ?',
 'Admission Data-Number of Patients awaiting admission with Confirmed or PUI COVID19 non-ventilated Response ?': 'Admission Data-Number of Patients awaiting admission with Confirmed or PUI COVID-19 non-ventilated Response ?',
 'COVID-19 Patient Counts-Number of patient deaths with Confirmed or PUI for COVID 19 in last 24 hours: ': 'COVID-19 Patient Counts-Number of patient deaths with Confirmed or PUI for COVID-19 in last 24 hours: '
}
