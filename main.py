#!/usr/bin/env python3
import argparse

import header_mapping as hm
from operators import process_csv
from agol_connection import AGOLConnection
from ingester import Ingester


def process_instantaneous(dry_run=False, datadir=None):
    print("Processing instantaneous tables...")

    errors = []
    if datadir is None:
        datadir = "/tmp"

    ingester = Ingester(dry_run)
    agol_connection = AGOLConnection()
    ingester.set_gis(agol_connection)

    # for now this part basically follows the same pattern as before, but work
    # should be done to consolidate the sftp and file management process.
    # the only difference is that now Ingester().get_files_from_sftp() is used.
    print("Getting latest HOS file from SFTP...")
    file_details, all_filenames = ingester.get_files_from_sftp(target_dir=datadir)
    data_dir = file_details[0]["dir"]
    latest_filename = file_details[0]["filename"]
    source_datetime = file_details[0]["source_datetime"]
    print("Finished.")

    # Public-only data
    public_processing_details = process_csv(
        [file_details[0]],
        output_prefix="public_processed_HOS_",
        columns_wanted=hm.columns_for_public_release,
        output_dir=datadir,
    )
    errors += public_processing_details['errors']
    public_processed_file_details = public_processing_details['file_details']
    public_processed_filename = public_processed_file_details[0]["processed_filename"]
    public_processed_dir = public_processed_file_details[0]["output_dir"]

    # Full data
    processing_details = process_csv(
        [file_details[0]],
        output_dir=datadir
    )
    errors += processing_details['errors']
    processed_file_details = processing_details['file_details']
    processed_filename = processed_file_details[0]["processed_filename"]
    processed_dir = processed_file_details[0]["output_dir"]

    print(f"Finished processing {data_dir}/{latest_filename}, file is {processed_dir}/{processed_filename}")

    # Use the new ingester methods, which are currently little more than wrappers
    # around the old methods. However, much less information must be passed to
    # them, as most info comes along with ingester. Future work can completely
    # migrate these functions from the old main file to the Ingester class.

    # process csv to update the non-public hospital table
    ingester.process_hospital(processed_dir, processed_filename, public=False)

    # process csv to update the public hospital table
    ingester.process_hospital(public_processed_dir, public_processed_filename)

    # process supplies
    ingester.process_supplies(processed_dir, processed_filename)

    ingester.process_county_summaries(processed_dir, processed_filename)
    print("Finished processing instantaneous tables.")

    errors += ingester.report_errors()
    return errors

def process_historical(dry_run=False, datadir=None, make_historical_csv=False):

    errors = []
    if datadir is None:
        datadir = "/tmp"

    ingester = Ingester(dry_run)
    agol_connection = AGOLConnection()
    ingester.set_gis(agol_connection)

    files_to_not_sftp = ingester.gis.get_already_processed_files("summary_table")
    file_details, all_filenames = ingester.get_files_from_sftp(target_dir=datadir, only_latest=False, filenames_to_ignore=files_to_not_sftp)

    if len(file_details) == 0:
        print("No new files to process for historical summary table data.")
    else:
        processing_details = process_csv(file_details, output_dir=datadir)
        errors += processing_details['errors']
        processed_file_details = processing_details['file_details']
        processed_dir = processed_file_details[0]["output_dir"]
        ingester.process_summaries(processed_dir, processed_file_details, make_historical_csv=make_historical_csv)

    files_to_not_sftp = ingester.gis.get_already_processed_files("full_historical_table")

    file_details, all_filenames = ingester.get_files_from_sftp(target_dir=datadir, only_latest=False, filenames_to_ignore=files_to_not_sftp)
    if len(file_details) == 0:
        print("No new files to process for historical data.")
    else:
        processing_details = process_csv(file_details, output_dir=datadir)
        errors += processing_details['errors']
        processed_file_details = processing_details['file_details']
        processed_dir = processed_file_details[0]["output_dir"]
        ingester.process_historical_hos(processed_dir, processed_file_details, make_historical_csv=make_historical_csv)


    print("Finished processing historical tables.")
    errors += ingester.report_errors()
    return errors


def process_canary_features(dry_run=False, datadir=None):
    print("Processing canary features...")
    if datadir is None:
        datadir = "/tmp"

    ingester = Ingester(dry_run)
    agol_connection = AGOLConnection()
    ingester.set_gis(agol_connection)

    print("XXX not doing historical averages yet")
    historical_gis_item_id = "3b39827f6f804c33b9b1114b5aa1d6b6" # v4
    historical_averages_item_id = ""
    ingester.process_daily_hospital_averages(historical_gis_item_id, historical_averages_item_id)
    print("Finished canary features.")

    # returning an empty list to maintain error reporting patterns
    return []

def main(dry_run, datadir=None, make_historical_csv=False):

    all_errors = []

    # all_errors += process_canary_features(dry_run=dry_run, datadir=datadir)
    all_errors += process_instantaneous(dry_run=dry_run, datadir=datadir)
    all_errors += process_historical(dry_run=dry_run, datadir=datadir, make_historical_csv=make_historical_csv)

    # at the very end of all processes, raise an exception if any errors have
    # been returned along the way. this will trigger the google cloud reporting.
    if len(all_errors) > 0:
        errors_str = "\n".join(list(set(all_errors)))
        raise Exception(errors_str)

def instantaneous_pubsub(event, context):
    print("Started instantaneous ingestion processing run")
    errors = process_instantaneous()
    print("Finished instantaneous ingestion processing run")

    if len(errors) > 0:
        errors_str = "\n".join(list(set(errors)))
        raise Exception(errors)

def historical_pubsub(event, context):
    print("Started historical ingestion processing run")
    errors = process_historical()
    print("Finished historical ingestion processing run")

    if len(errors) > 0:
        errors_str = "\n".join(list(set(errors)))
        raise Exception(errors)

if __name__== "__main__":
    make_historical_csv = False
    dry_run = False
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry_run")
    parser.add_argument("--dir")
    parser.add_argument("--make_historical_csv")
    args = parser.parse_args()
    if args.dry_run is not None:
        dry_run = True
    if args.make_historical_csv is not None:
        make_historical_csv = True
    print(f"dry_run: {dry_run}")
    main(dry_run, datadir=args.dir, make_historical_csv=make_historical_csv)
