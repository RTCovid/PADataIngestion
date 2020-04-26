from datetime import datetime


def get_datetime_from_filename(filename, prefix="HOS_ResourceCapacity_"):
    source_date = filename.split('.')[0]
    source_date = source_date.replace(prefix,'')
    source_date = source_date + " UTC"
    source_date = datetime.strptime(source_date, "%Y-%m-%d_%H-%M %Z")
    return source_date

