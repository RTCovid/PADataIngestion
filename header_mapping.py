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
            values += v['aliases']
        return values

    def get_fieldnames(self):
        """This is a list of all valid short fieldnames. Most useful for testing."""

        return list(self.mapping.keys())

    def get_fieldnames_and_aliases(self):
        """Creates one big list of all fieldnames and all aliases."""

        return self.get_fieldnames() + self.get_aliases()

    def get_master_lookup(self):
        """This lookup has keys for all long names AND all short names. Each key
        corresponds to the proper short name. Allows a single point of entry for
        any header name."""

        lookup = {}
        for k, v in self.mapping.items():
            lookup[k] = k
            for alias in v['aliases']:
                lookup[alias] = k

        return lookup

    def get_public_column_names(self):
        """returns the names of all columns in the mapping that have been marked
        'public' = True"""

        cols = list()
        for k, v in self.mapping.items():
            if v.get("public", False) is True:
                cols.append(k)

        return cols


ltc_mapping = {}

hos_mapping = {
    'hospitalname': {
        'aliases': [
            'HospitalName',
            'hospitalName',
        ],
        'public': True,
    },
    'hospitalstreetaddress': {
        'aliases': [
            'HospitalStreetAddress',
            'hospitalStreetAddress',
        ],
        'public': True,
    },
    'hospitalcity': {
        'aliases': [
            'HospitalCity',
            'hospitalCity',
        ],
        'public': True,
    },
    'hospitalstate': {
        'aliases': [
            'HospitalState',
            'hospitalState',
        ],
        'public': True,
    },
    'hospitalzip': {
        'aliases': [
            'HospitalZip',
            'hospitalZip',
        ],
        'public': True,
    },
    'hospitallatitude': {
        'aliases': [
            'HospitalLatitude',
            'hospitalLatitude',
        ],
        'public': True,
    },
    'hospitallongitude': {
        'aliases': [
            'HospitalLongitude',
            'hospitalLongitude',
        ],
        'public': True,
    },
    'numicubeds': {
        'aliases': [
            'Available Beds-Adult Intensive Care Unit (ICU) Staffed Beds',
        ],
        'public': True,
    },
    'icuavail': {
        'aliases': [
            'Available Beds-Adult Intensive Care Unit (ICU) Current Available',
        ],
        'public': True,
    },
    'icu24h': {
        'aliases': [
            'Available Beds-Adult Intensive Care Unit (ICU) 24hr Beds',
        ],
        'public': True,
    },
    'icu72h': {
        'aliases': [
            'Available Beds-Adult Intensive Care Unit (ICU) 72hr Beds',
        ],
        'public': True,
    },
    'medsurgstaff': {
        'aliases': [
            'Available Beds-Medical and Surgical (Med/Surg) Staffed Beds',
        ],
        'public': True,
    },
    'medsurgavail': {
        'aliases': [
            'Available Beds-Medical and Surgical (Med/Surg) Current Available',
        ],
        'public': True,
    },
    'medsurg24h': {
        'aliases': [
            'Available Beds-Medical and Surgical (Med/Surg) 24hr Beds',
        ],
        'public': True,
    },
    'medsurg72h': {
        'aliases': [
            'Available Beds-Medical and Surgical (Med/Surg) 72hr Beds',
        ],
        'public': True,
    },
    'burnstaff': {
        'aliases': [
            'Available Beds-Burn Staffed Beds',
        ],
    },
    'burnavail': {
        'aliases': [
            'Available Beds-Burn Current Available',
        ],
    },
    'burn24h': {
        'aliases': [
            'Available Beds-Burn 24hr Beds',
        ],
    },
    'burn72h': {
        'aliases': [
            'Available Beds-Burn 72hr Beds',
        ],
    },
    'picstaff': {
        'aliases': [
            'Available Beds-Pediatric Intensive Care Staffed Beds',
        ],
        'public': True,
    },
    'picavail': {
        'aliases': [
            'Available Beds-Pediatric Intensive Care Current Available',
        ],
        'public': True,
    },
    'pic24h': {
        'aliases': [
            'Available Beds-Pediatric Intensive Care 24hr Beds',
        ],
        'public': True,
    },
    'pic72h': {
        'aliases': [
            'Available Beds-Pediatric Intensive Care 72hr Beds',
        ],
        'public': True,
    },
    'pedstaff': {
        'aliases': [
            'Available Beds-Pediatric Staffed Beds',
        ],
        'public': True,
    },
    'pedavail': {
        'aliases': [
            'Available Beds-Pediatric Current Available',
        ],
        'public': True,
    },
    'ped24h': {
        'aliases': [
            'Available Beds-Pediatric 24hr Beds',
        ],
        'public': True,
    },
    'ped72h': {
        'aliases': [
            'Available Beds-Pediatric 72hr Beds',
        ],
        'public': True,
    },
    'nicustaff': {
        'aliases': [
            'Available Beds-Neonatal Staffed Beds',
        ],
    },
    'nicuavail': {
        'aliases': [
            'Available Beds-Neonatal Current Available',
        ],
    },
    'nicu24h': {
        'aliases': [
            'Available Beds-Neonatal 24hr Beds',
        ],
    },
    'nicu72h': {
        'aliases': [
            'Available Beds-Neonatal 72hr Beds',
        ],
    },
    'rehabstaff': {
        'aliases': [
            'Available Beds-Inpatient Rehab Staffed Beds',
        ],
    },
    'rehabavail': {
        'aliases': [
            'Available Beds-Inpatient Rehab Current Available',
        ],
    },
    'rehab24h': {
        'aliases': [
            'Available Beds-Inpatient Rehab 24hr Beds',
        ],
    },
    'rehab72h': {
        'aliases': [
            'Available Beds-Inpatient Rehab 72hr Beds',
        ],
    },
    'psychstaff': {
        'aliases': [
            'Psych Beds-Psychiatric Staffed Beds',
        ],
    },
    'psychavail': {
        'aliases': [
            'Psych Beds-Psychiatric Current Available',
        ],
    },
    'psych24h': {
        'aliases': [
            'Psych Beds-Psychiatric 24hr Beds',
        ],
    },
    'psych72h': {
        'aliases': [
            'Psych Beds-Psychiatric 72hr Beds',
        ],
    },
    'psychadultstaff': {
        'aliases': [
            'Psych Beds-Adult Staffed Beds',
        ],
    },
    'psychadultavail': {
        'aliases': [
            'Psych Beds-Adult Current Available',
        ],
    },
    'psychadult24h': {
        'aliases': [
            'Psych Beds-Adult 24hr Beds',
        ],
    },
    'psychadult72h': {
        'aliases': [
            'Psych Beds-Adult 72hr Beds',
        ],
    },
    'psychadolstaff': {
        'aliases': [
            'Psych Beds-Adolescent Staffed Beds',
        ],
    },
    'psychadolavail': {
        'aliases': [
            'Psych Beds-Adolescent Current Available',
        ],
    },
    'psychadol24h': {
        'aliases': [
            'Psych Beds-Adolescent 24hr Beds',
        ],
    },
    'psychadol72h': {
        'aliases': [
            'Psych Beds-Adolescent 72hr Beds',
        ],
    },
    'psychgeristaff': {
        'aliases': [
            'Psych Beds-Geriatric Staffed Beds',
        ],
    },
    'psychgeriavail': {
        'aliases': [
            'Psych Beds-Geriatric Current Available',
        ],
    },
    'psychgeri24h': {
        'aliases': [
            'Psych Beds-Geriatric 24hr Beds',
        ],
    },
    'psychgeri72h': {
        'aliases': [
            'Psych Beds-Geriatric 72hr Beds',
        ],
    },
    'psychmeddetoxstaff': {
        'aliases': [
            'Psych Beds-Medical Detox Staffed Beds',
        ],
    },
    'psychmeddetoxavail': {
        'aliases': [
            'Psych Beds-Medical Detox Current Available',
        ],
    },
    'psychmeddetox24h': {
        'aliases': [
            'Psych Beds-Medical Detox 24hr Beds',
        ],
    },
    'psychmeddetox72h': {
        'aliases': [
            'Psych Beds-Medical Detox 72hr Beds',
        ],
    },
    'psychsaddstaff': {
        'aliases': [
            'Psych Beds-Substance Abuse (Dual Diagnosis) Staffed Beds',
        ],
    },
    'psychsaddavail': {
        'aliases': [
            'Psych Beds-Substance Abuse (Dual Diagnosis) Current Available',
        ],
    },
    'psychsadd24h': {
        'aliases': [
            'Psych Beds-Substance Abuse (Dual Diagnosis) 24hr Beds',
        ],
    },
    'psychsadd72h': {
        'aliases': [
            'Psych Beds-Substance Abuse (Dual Diagnosis) 72hr Beds',
        ],
    },
    'labordelivstaff': {
        'aliases': [
            'Other Beds-Labor / Delivery Staffed Beds',
        ],
    },
    'labordelivavail': {
        'aliases': [
            'Other Beds-Labor / Delivery Current Available',
        ],
    },
    'labordeliv24h': {
        'aliases': [
            'Other Beds-Labor / Delivery 24hr Beds',
        ],
    },
    'labordeliv72h': {
        'aliases': [
            'Other Beds-Labor / Delivery 72hr Beds',
        ],
    },
    'maternitystaff': {
        'aliases': [
            'Other Beds-Maternity / Newborn Nursery Staffed Beds',
        ],
    },
    'maternityavail': {
        'aliases': [
            'Other Beds-Maternity / Newborn Nursery Current Available',
        ],
    },
    'maternity24h': {
        'aliases': [
            'Other Beds-Maternity / Newborn Nursery 24hr Beds',
        ],
    },
    'maternity72h': {
        'aliases': [
            'Other Beds-Maternity / Newborn Nursery 72hr Beds',
        ],
    },
    'aiistaff': {
        'aliases': [
            'Other Beds-Airborne Infection Isolation Staffed Beds',
        ],
        'public': True,
    },
    'aiiavail': {
        'aliases': [
            'Other Beds-Airborne Infection Isolation Current Available',
        ],
        'public': True,
    },
    'aii24h': {
        'aliases': [
            'Other Beds-Airborne Infection Isolation 24hr Beds',
        ],
        'public': True,
    },
    'aii72h': {
        'aliases': [
            'Other Beds-Airborne Infection Isolation 72hr Beds',
        ],
        'public': True,
    },
    'edimmediate': {
        'aliases': [
            'Emergency Department-ED Available Capacity Immediate',
        ],
    },
    'eddelayed': {
        'aliases': [
            'Emergency Department-ED Available Capacity Delayed',
        ],
    },
    'edminor': {
        'aliases': [
            'Emergency Department-ED Available Capacity Minor',
        ],
    },
    'eddeceased': {
        'aliases': [
            'Emergency Department-ED Available Capacity Deceased',
        ],
    },
    'noncvd19pntadmit': {
        'aliases': [
            'Admission Data-Number of Patients awaiting admission Non COVID-19 Response ?',
            'Admission Data-Number of Patients awaiting admission Response ?',
        ],
    },
    'cvd19pntadmitnonvent': {
        'aliases': [
            'Admission Data-Number of Patients awaiting admission with Confirmed or PUI COVID-19 non-ventilated Response ?',
            'Admission Data-Number of Patients awaiting admission with Confirmed or PUI COVID19 non-ventilated Response ?',
        ],
    },
    'cvd19pntadmitnvent': {
        'aliases': [
            'Admission Data-Number of Patients awaiting admission for Confirmed or PUI COVID-19 on ventilator Response ?',
            'Admission Data-Number of Patients awaiting admission for Confirmed or PUI COVID 19 on ventilator Response ?',
        ],
    },
    'pntadmiticu': {
        'aliases': [
            'Admission Data-Number of Patients awaiting ICU Bed Response ?',
        ],
    },
    'pntdischrg': {
        'aliases': [
            'Admission Data-Number of Patients awaiting discharge placement Response ?',
        ],
    },
    'facrespplan': {
        'aliases': [
            'EEIs-Does your facility have an established respiratory protection plan? Response ?',
        ],
    },
    'n95fittested': {
        'aliases': [
            'EEIs-Is your facility planning to use N95 masks. If so is your staff fit-tested to wear N95 masks? Response ?',
        ],
    },
    'modelsfittested': {
        'aliases': [
            'EEIs-What mask brands and models are staff fit tested to use? Response ?',
        ],
    },
    'paprtrained': {
        'aliases': [
            'EEIs-Is your facility planning to use PAPRs. If so is your staff trained to use PAPRs? Response ?',
        ],
    },
    'ppedondoff': {
        'aliases': [
            'EEIs-Is your staff adequately trained in correctly donning and doffing of PPE? Response ?',
        ],
    },
    'needsanitizer': {
        'aliases': [
            'Is there an immediate need for hand hygiene/disinfection supplies listed below?-Alcohol Based Hand Sanitizer Response ?',
        ],
    },
    'needhandsoap': {
        'aliases': [
            'Is there an immediate need for hand hygiene/disinfection supplies listed below?-Hand Soap Response ?',
        ],
    },
    'needsolution': {
        'aliases': [
            'Is there an immediate need for hand hygiene/disinfection supplies listed below?-Disinfection Solutions Response ?',
        ],
    },
    'needwipes': {
        'aliases': [
            'Is there an immediate need for hand hygiene/disinfection supplies listed below?-Disinfection Wipes Response ?',
        ],
    },
    'needgloves': {
        'aliases': [
            'Is there an immediate need for hand hygiene/disinfection supplies listed below?-Gloves Response ?',
        ],
    },
    'needother1': {
        'aliases': [
            'Is there an immediate need for hand hygiene/disinfection supplies listed below?-Other (please specify) Response ?',
        ],
    },
    'needn95': {
        'aliases': [
            "Does your facility anticipate material/supply shortages of the following?-N95's Response ?",
        ],
    },
    'needpapr': {
        'aliases': [
            "Does your facility anticipate material/supply shortages of the following?-PAPR's Response ?",
        ],
    },
    'needpaprhoods': {
        'aliases': [
            "Does your facility anticipate material/supply shortages of the following?-PAPR's Hoods Response ?",
        ],
    },
    'needpaprfilters': {
        'aliases': [
            "Does your facility anticipate material/supply shortages of the following?-PAPR's Filters Response ?",
        ],
    },
    'needmasks': {
        'aliases': [
            'Does your facility anticipate material/supply shortages of the following?-Facial Masks (Procedural/Surgical) Response ?',
        ],
    },
    'needgown': {
        'aliases': [
            'Does your facility anticipate material/supply shortages of the following?-Gown/Apron Response ?',
        ],
    },
    'needeyepro': {
        'aliases': [
            'Does your facility anticipate material/supply shortages of the following?-Eye Protection (Goggles Face shield) Response ?',
        ],
    },
    'needcleaning': {
        'aliases': [
            'Does your facility anticipate material/supply shortages of the following?-Cleaning/Disinfection Supplies Response ?',
        ],
    },
    'needother2': {
        'aliases': [
            'Does your facility anticipate material/supply shortages of the following?-Other (please specify) Response ?',
        ],
    },
    'shortn95': {
        'aliases': [
            "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-N95's Response ?",
        ],
    },
    'shortpapr': {
        'aliases': [
            "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-PAPR's Response ?",
        ],
    },
    'shortpaprhoods': {
        'aliases': [
            "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-PAPR's Hoods Response ?",
        ],
    },
    'shortpaprfilters': {
        'aliases': [
            "If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-PAPR's Filters Response ?",
        ],
    },
    'shortmasks': {
        'aliases': [
            'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Facial Masks (Procedural/Surgical) Response ?',
        ],
    },
    'shortgowns': {
        'aliases': [
            'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Gowns Response ?',
        ],
    },
    'shorteyepro': {
        'aliases': [
            'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Eye Protection (Goggles Face shield) Response ?',
        ],
    },
    'shortsoap': {
        'aliases': [
            'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Hand Soap Response ?',
        ],
    },
    'shortsanitizer': {
        'aliases': [
            'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Hand Sanitizer Response ?',
        ],
    },
    'shortcleaning': {
        'aliases': [
            'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Cleaning/Disinfection Supplies Response ?',
        ],
    },
    'shortother1': {
        'aliases': [
            'If you have a COVID-19 resident(s) Do you anticipate shortages of the below:-Other (please specify) Response ?',
        ],
    },
    'burnn95': {
        'aliases': [
            "Current Burn Rates per day for the following PPE (Single Units):-N95's Response ?",
        ],
    },
    'burnpapr': {
        'aliases': [
            "Current Burn Rates per day for the following PPE (Single Units):-PAPR's Response ?",
        ],
    },
    'burnpaprhoods': {
        'aliases': [
            "Current Burn Rates per day for the following PPE (Single Units):-PAPR's Hoods Response ?",
        ],
    },
    'burnpaprfilter': {
        'aliases': [
            "Current Burn Rates per day for the following PPE (Single Units):-PAPR's Filters Response ?",
        ],
    },
    'burnmask': {
        'aliases': [
            'Current Burn Rates per day for the following PPE (Single Units):-Facial Masks (Procedural/Surgical) Response ?',
        ],
    },
    'burngowns': {
        'aliases': [
            'Current Burn Rates per day for the following PPE (Single Units):-Gowns Response ?',
        ],
    },
    'burneyepro': {
        'aliases': [
            'Current Burn Rates per day for the following PPE (Single Units):-Eye Protection (Goggles Face shield) Response ?',
        ],
    },
    'shortcollection': {
        'aliases': [
            'Testing Supplies-What diagnostic testing or specimen collection supplies do you anticipate a shortage of? ',
        ],
    },
    'shortother2': {
        'aliases': [
            'Testing Supplies-Other (please specify) ',
        ],
    },
    'testlocal': {
        'aliases': [
            'Local Testing-Do you have a commercial or inhouse platform for performing local testing of COVID-19? ',
        ],
    },
    'date': {
        'aliases': [
            'Local Testing-Real or future go-live date: ',
        ],
    },
    'cvd19tstrun': {
        'aliases': [
            'Local Testing-How many COVID-19 tests were run at your inhouse lab today? ',
            'How many COVID-19 tests were run at your inhouse lab today? ',
        ],
    },
    'cvd19tstpostve': {
        'aliases': [
            'Local Testing-How many of those inhouse tests were positive? ',
            'How many of those inhouse tests were positive? ',
        ],
    },
    'numc19hosppats': {
        'aliases': [
            'COVID-19 Patient Counts-Total number of inpatients diagnosed with COVID-19: ',
            'COVID-19 Patient Counts-Total number of inpatients diagnosed with COVID-19:',
        ],
        'public': True,
    },
    'ttlcvd19pui': {
        'aliases': [
            'COVID-19 Patient Counts-Total number of inpatients under suspicion for COVID-19 (PUI): ',
            'COVID-19 Patient Counts-Total number of inpatients under suspicion for COVID-19 (PUI):',
        ],
        'public': True,
    },
    'ttlnumicubedscvd19': {
        'aliases': [
            'COVID-19 Patient Counts - Total number of ICU beds occupied by a diagnosed COVID-19 patient:',
            'COVID-19 Patient Counts-Total number of ICU beds occupied by a diagnosed COVID-19 patient: ',
            'COVID-19 Patient Counts-Total number of ICU beds occupied by a diagnosed COVID-19 patient:',
        ],
    },
    'cvdnumc19hopats': {
        'aliases': [
            'COVID-19 Patient Counts-Total number of inpatients admitted 14+ days for other conditions now PUI or confirmed COVID-19?: ',
            'COVID-19 Patient Counts-Total number of inpatients admitted 14+ days for other conditions now PUI or confirmed COVID-19?:',
        ],
    },
    'numc19mechventpats': {
        'aliases': [
            'COVID-19 Patient Counts-Total number of inpatients diagnosed with COVID-19 on ventilators: ',
            'COVID-19 Patient Counts-Total number of patients diagnosed with COVID-19 on ventilators: ',
            'COVID-19 Patient Counts-Total number of patients diagnosed with COVID-19 on ventilators:',
        ],
        'public': True,
    },
    'ttlcvd19ptntecmo': {
        'aliases': [
            'COVID-19 Patient Counts-Total number of inpatients diagnosed with COVID-19 on ECMO: ',
            'COVID-19 Patient Counts-Total number of patients diagnosed with COVID-19 on ECMO: ',
            'COVID-19 Patient Counts-Total number of patients diagnosed with COVID-19 on ECMO:',
        ],
        'public': True,
    },
    'ttlaiied': {
        'aliases': [
            'COVID-19 Patient Counts-How many airborne infection isolation rooms are in your ED? ',
            'COVID-19 Patient Counts-How many airborne infection isolation rooms are in your ED?',
        ],
        'public': True,
    },
    'ttlaiiicu': {
        'aliases': [
            'COVID-19 Patient Counts-How many airborne infection isolation rooms are in your ICU? ',
            'COVID-19 Patient Counts-How many airborne infection isolation rooms are in your ICU?',
        ],
        'public': True,
    },
    'ttlaiinonicu': {
        'aliases': [
            'COVID-19 Patient Counts-How many airborne infection isolation rooms are in non-ICU? ',
            'COVID-19 Patient Counts-How many airborne infection isolation rooms are in non-ICU?',
        ],
        'public': True,
    },
    'cvdnumc19died': {
        'aliases': [
            'COVID-19 Patient Counts-Number of patient deaths with Confirmed or PUI for COVID-19 in last 24 hours: ',
            'COVID-19 Patient Counts-Number of patient deaths with Confirmed or PUI for COVID 19 in last 24 hours: ',
            'COVID-19 Patient Counts-Number of patient deaths with Confirmed or PUI for COVID 19 in last 24 hours:',
        ],
    },
    'conspperesp': {
        'aliases': [
            'Are you currently implementing conservation strategies to preserve PPE:-Extended use of respirators Response ?',
        ],
    },
    'consppereuseresp': {
        'aliases': [
            'Are you currently implementing conservation strategies to preserve PPE:-Use of reusable respirators in place of disposable N95s (i.e. PAPRs elastomeric N95s etc.) Response ?',
        ],
    },
    'consppedispon95': {
        'aliases': [
            'Are you currently implementing conservation strategies to preserve PPE:-Reuse of disposable N95 respirators Response ?',
        ],
    },
    'consppestaffhours': {
        'aliases': [
            'Are you currently implementing conservation strategies to preserve PPE:-Extended staff hours/shifts Response ?',
        ],
    },
    'consppecohortwodestaff': {
        'aliases': [
            'Are you currently implementing conservation strategies to preserve PPE:-Cohorting patients without dedicated staff Response ?',
        ],
    },
    'consppecohortwdestaff': {
        'aliases': [
            'Are you currently implementing conservation strategies to preserve PPE:-Cohorting patients with dedicated staff Response ?',
        ],
    },
    'n95utli3less': {
        'aliases': [
            'n95masksupply3less',
            'At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-3 or less days Response ?',
        ],
    },
    'n95utli47': {
        'aliases': [
            'n95util47',
            'At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-4-7 days Response ?',
        ],
    },
    'n95util814': {
        'aliases': [
            'At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-8-14 days Response ?',
        ],
    },
    'n95util1528': {
        'aliases': [
            'At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-15-28 days Response ?',
        ],
    },
    'n95util29more': {
        'aliases': [
            'At current utilization rates how long do you expect your current supply of N95 respirators to last at your facility?-29 or more days Response ?',
        ],
    },
    'ppeutli3less': {
        'aliases': [
            'At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-3 or less days Response ?',
        ],
    },
    'ppeutli47': {
        'aliases': [
            'At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-4-7 days Response ?',
        ],
    },
    'ppeutil814': {
        'aliases': [
            'At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-8-14 days Response ?',
        ],
    },
    'ppeutil1528': {
        'aliases': [
            'At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-15-28 days Response ?',
        ],
    },
    'ppeutil29more': {
        'aliases': [
            'At current utilization rates how long do you expect your current supply of other PPE (gowns gloves etc) to last at your facility?-29 or more days Response ?',
        ],
    },
    'nputli3less': {
        'aliases': [
            'At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-3 or less days Response ?',
        ],
    },
    'nputli47': {
        'aliases': [
            'At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-4-7 days Response ?',
        ],
    },
    'nputil814': {
        'aliases': [
            'At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-8-14 days Response ?',
        ],
    },
    'nputil1528': {
        'aliases': [
            'At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-15-28 days Response ?',
        ],
    },
    'nputil29more': {
        'aliases': [
            'At current utilization rates how long do you expect your current supply of NP specimen collection supplies to last at your facility?-29 or more days Response ?',
        ],
    },
    'ttlempcall': {
        'aliases': [
            'Employee Status-Total Employee Call Outs/Absenteeism ',
        ],
    },
    'ttlempcvd19': {
        'aliases': [
            'Employee Status-Call out reason: sick with COVID-19 ',
        ],
    },
    'ttlcalloutphys': {
        'aliases': [
            'Employee Status-Number of Call Outs that are Physicians ',
        ],
    },
    'ttlcalloutnurse': {
        'aliases': [
            'Employee Status-Number of Call Outs that are Nurses ',
        ],
    },
    'ttlcalloutisolation': {
        'aliases': [
            'Employee Status-Call out reason: quarantine or isolation due to exposure ',
        ],
    },
    'ttlcalloutchildcare': {
        'aliases': [
            'Employee Status-Call out reason: child care issues ',
        ],
    },
    'envrnmntlsrvcsday': {
        'aliases': [
            'Critical Staffing Shortages Today?-Environmental Services Response ?',
            'Todays Critical Staffing Shortages - Environmental Services',
        ],
    },
    'rnlpnday': {
        'aliases': [
            'Critical Staffing Shortages Today?-Nurses: RN and LPNs Response ?',
            'Todays Critical Staffing Shortages -Nurses: RN and LPNs',
        ],
    },
    'rsprtrythrpstday': {
        'aliases': [
            'Critical Staffing Shortages Today?-Respritory Therapists Response ?',
            'Todays Critical Staffing Shortages -Respritory Therapists',
        ],
    },
    'phtmcstday': {
        'aliases': [
            'Critical Staffing Shortages Today?-Pharmacists and Pharmacy Techs Response ?',
            'Todays Critical Staffing Shortages -Pharmacists and Pharmacy Techs',
        ],
    },
    'physcnstday': {
        'aliases': [
            'Critical Staffing Shortages Today?-Physicans: Attending Fellows Response ?',
            'Todays Critical Staffing Shortages -Physicans: Attending, Fellows',
        ],
    },
    'otherindpendtday': {
        'aliases': [
            'Critical Staffing Shortages Today?-Other licensed independent practitioners: Advanced Practice Nurses Physician Assistances Response ?',
            'Todays Critical Staffing Shortages -Other licensed independent practitioners: Advanced Practice Nurses, Physician Assistances',
        ],
    },
    'tempday': {
        'aliases': [
            'Critical Staffing Shortages Today?-Temporary physicians nurse etc (per diems travelers retired seasonal) Response ?',
            'Todays Critical Staffing Shortages -Temporary physicians, nurse, etc (per diems, travelers, retired, seasonal)',
        ],
    },
    'otherhcpday': {
        'aliases': [
            'Critical Staffing Shortages Today?-Other HCP Personnel (Other persons who work in the facilities not detailed above Response ?',
            'Todays Critical Staffing Shortages -Other HCP Personnel (Other persons who work in the facilities not detailed above',
        ],
    },
    'otherhcpdaylist': {
        'aliases': [
            'Critical Staffing Shortages Today?-What other HCP Personnel not listed above do you have a critical staff shortage of? Response ?',
            'Todays Critical Staffing Shortages -What other HCP Personnel not listed above do you have a critical staff shortage of? ',
        ],
    },
    'envrnmntlsrvcsweek': {
        'aliases': [
            'Critical Staffing Shortages within a week?-Environmental Services Response ?',
            'Forecasted Critical Staffing Shortages - Environmental Services',
        ],
    },
    'rnlpnweek': {
        'aliases': [
            'Critical Staffing Shortages within a week?-Nurses: RN and LPNs Response ?',
            'Forecasted Critical Staffing Shortages -Nurses: RN and LPNs',
        ],
    },
    'rsprtrythrpstweek': {
        'aliases': [
            'Critical Staffing Shortages within a week?-Respritory Therapists Response ?',
            'Forecasted Critical Staffing Shortages -Respritory Therapists',
        ],
    },
    'phtmcstweek': {
        'aliases': [
            'Critical Staffing Shortages within a week?-Pharmacists and Pharmacy Techs Response ?',
            'Forecasted Critical Staffing Shortages -Pharmacists and Pharmacy Techs',
        ],
    },
    'physcnstweek': {
        'aliases': [
            'Critical Staffing Shortages within a week?-Physicans: Attending Fellows Response ?',
            'Forecasted Critical Staffing Shortages -Physicans: Attending, Fellows',
        ],
    },
    'otherindpendtweek': {
        'aliases': [
            'Critical Staffing Shortages within a week?-Other licensed independent practitioners: Advanced Practice Nurses Physician Assistances Response ?',
            'Forecasted Critical Staffing Shortages -Other licensed independent practitioners: Advanced Practice Nurses, Physician Assistances',
        ],
    },
    'tempweek': {
        'aliases': [
            'Critical Staffing Shortages within a week?-Temporary physicians nurse etc (per diems travelers retired seasonal) Response ?',
            'Forecasted Critical Staffing Shortages -Temporary physicians, nurse, etc (per diems, travelers, retired, seasonal)',
        ],
    },
    'otherhcpweek': {
        'aliases': [
            'Critical Staffing Shortages within a week?-Other HCP Personnel (Other persons who work in the facilities not detailed above Response ?',
            'Forecasted Critical Staffing Shortages -Other HCP Personnel (Other persons who work in the facilities not detailed above',
        ],
    },
    'otherhcpweeklist': {
        'aliases': [
            'Critical Staffing Shortages within a week?-What other HCP Personnel not listed above do you have a critical staff shortage of? Response ?',
            'Forecasted Critical Staffing Shortages -What other HCP Personnel not listed above do you have a critical staff shortage of? ',
        ],
    },
    'numvent': {
        'aliases': [
            'Ventilator Counts-Ventilators Number of ventilators',
        ],
        'public': True,
    },
    'numventuse': {
        'aliases': [
            'Ventilator Counts-Ventilators Number of ventilators in use',
        ],
        'public': True,
    },
    'numanesthesia': {
        'aliases': [
            'Ventilator Counts-Ventilators Number of Anesthesia Machines',
            'Ventilator Counts-Ventilators Number of Anestesia Machines',
        ],
        'public': True,
    },
    'numanesthesiaconvert': {
        'aliases': [
            'Ventilator Counts-Ventilators Number of Anesthesia Machines that are converted to be used as a Vent',
            'Ventilator Counts-Ventilators Number of Anestesia Machines that are converted to be used as a Vent',
        ],
        'public': True,
    },
    'numcvd19onvent': {
        'aliases': [
            'Ventilator Usage-Ventilators Number of ventilators used for COVID-19 patients (confirmed)',
        ],
    },
    'numecmo': {
        'aliases': [
            'Ventilator Usage-Ventilators ECMO units',
        ],
    },
    'numecmouse': {
        'aliases': [
            'Ventilator Usage-Ventilators ECMO units in use',
        ],
    },
    'numecmocvd19': {
        'aliases': [
            'Ventilator Usage-Ventilators ECMO units in use for COVID-19 patients',
        ],
    },
    'aiiedtotal': {
        'aliases': [
            'Airborne Isolation Rooms-ED Total',
        ],
    },
    'aiiedavailable': {
        'aliases': [
            'Airborne Isolation Rooms-ED Available',
        ],
    },
    'aiiedoccupied': {
        'aliases': [
            'Airborne Isolation Rooms-ED Occupied requiring airborne isolation',
        ],
    },
    'aiiedoccupiedcvd19': {
        'aliases': [
            'Airborne Isolation Rooms-ED Occupied by COVID-19 patient',
        ],
    },
    'aiinonicutotal': {
        'aliases': [
            'Airborne Isolation Rooms-Inpatient non-ICU Total',
        ],
    },
    'aiinonicuavail': {
        'aliases': [
            'Airborne Isolation Rooms-Inpatient non-ICU Available',
        ],
    },
    'aiinonicuoccupied': {
        'aliases': [
            'Airborne Isolation Rooms-Inpatient non-ICU Occupied requiring airborne isolation',
        ],
    },
    'aiinonicuoccupiedcvd19': {
        'aliases': [
            'Airborne Isolation Rooms-Inpatient non-ICU Occupied by COVID-19 patient',
        ],
    },
    'aiiicutotal': {
        'aliases': [
            'Airborne Isolation Rooms-ICU Total',
        ],
    },
    'aiiicuavail': {
        'aliases': [
            'Airborne Isolation Rooms-ICU Available',
        ],
    },
    'aiiicuoccupied': {
        'aliases': [
            'Airborne Isolation Rooms-ICU Occupied requiring airborne isolation',
        ],
    },
    'aiiicuoccupiedcvd19': {
        'aliases': [
            'Airborne Isolation Rooms-ICU Occupied by COVID-19 patient',
        ],
    },

    # Fields added by these scripts that we know are valid.
    'HospitalCounty': {
        'aliases': [
            'HospitalCounty',
        ],
    },
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
        "n": "icuavail",
        "d": "numicubeds" ,
    },
    "Percent Available Med/Surg Beds":
    {
        "n": "medsurgavail",
        "d": "medsurgstaff",
    },
    "Percent Available Beds Pediatric Intensive Care":
    {
        "n": "picavail",
        "d": "picstaff",
    },
    "Percent Available Pediatric Beds": {
        "n": "pedavail",
        "d": "pedstaff",
    },
    "Percent Available Airborne Isolation Bed":
    {
        "n": "aiiavail",
        "d": "aiistaff",
    }
}

supplies_on_hand_headers = {
    "3": "Less Than 3 Days",
    "7": "4 to 7 Days",
    "14": "8 to 14 Days",
    "28": "15 to 28 Days",
    "29": "Greater than 29 Days",
}

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
