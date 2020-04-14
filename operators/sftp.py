import pysftp
import glob
import os
from datetime import datetime


def get_datetime_from_filename(filename, prefix="HOS_ResourceCapacity_"):
    source_date = filename.split('.')[0]
    source_date = source_date.replace(prefix,'')
    source_date = source_date + " UTC"
    source_date = datetime.strptime(source_date, "%Y-%m-%d_%H-%M %Z")
    return source_date

# On Google Cloud, only /tmp is writeable.
def get_files_from_sftp(creds, prefix="HOS_ResourceCapacity_", target_dir="/tmp", 
                               only_latest=True, filenames_to_ignore=[]):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys.load('copaftp.pub')
    username = creds['sftp']['username']
    password = creds['sftp']['password']
    host = creds['sftp']['host']
    latest_filename = ""
    files = ""
    file_details = []

    existing_files = glob.glob(target_dir + "/" + prefix + "*")

    with pysftp.Connection(host, username=username, password=password, cnopts=cnopts) as sftp:
        files = sftp.listdir()
        files = [f for f in files if f.startswith(prefix)]
        # the files are sorted by the pysftp library, and the last element of the list is the latest file
        # Filenames look like HOS_ResourceCapacity_2020-03-30_00-00.csv
        # And timestamps are in UTC
        files_to_get = []
        if only_latest:
            latest_filename = files[-1]
            files_to_get = [latest_filename]
        else:
            files_to_get = files
        for f in files_to_get:
            if f in filenames_to_ignore:
                print(f"Ignoring {f}")
                continue
            print(f"Getting: {f}")
            if os.path.join(target_dir, f) not in existing_files:
                sftp.get(f, f'{target_dir}/{f}')
                print(f"Finished downloading {target_dir}/{f}")
            else:
                print(f"Didn't have to download {target_dir}/{f}; it already exists")

            source_date = get_datetime_from_filename(f, prefix=prefix)
            file_details.append({"dir": target_dir, "filename": f, "source_datetime": source_date})
    return (file_details, files)

