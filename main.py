#!/usr/bin/env python3
import os
import argparse

import header_mapping as hm
from operators import process_csv
from agol_connection import AGOLConnection
from validator import CSVValidator
from ingester import Ingester


    print("Processing instantaneous tables...")
def process_instantaneous(dry_run=False, datadir=None, verbose=False):

    if datadir is None:
        datadir = "/tmp"

    ingester = Ingester(dry_run, verbose=verbose)

    # for now this part basically follows the same pattern as before, but work
    # should be done to consolidate the sftp and file management process.
    # the only difference is that now Ingester().get_files_from_sftp() is used.
    print("Getting latest HOS file from SFTP...")
    file_details, all_filenames = ingester.get_files_from_sftp(target_dir=datadir)
    print("Finished.")

    latest_file_details = file_details[0]

    # run a validation on the latest file (the one that will be used for instantaneous)
    # validate_csv() will raise an exception if it fails. use raise_exception=False
    # to run it quietly.
    v = CSVValidator("HOS")
    fpath = os.path.join(latest_file_details['dir'], latest_file_details['filename'])
    v.validate_csv(fpath)

    # validation passed on downloaded file, now do all processing

    # Public-only data
    public_processed_file_details = process_csv(
        [latest_file_details],
        output_prefix="public_processed_HOS_",
        columns_wanted=hm.columns_for_public_release,
        output_dir=datadir,
    )
    public_processed_filename = public_processed_file_details[0]["processed_filename"]
    public_processed_dir = public_processed_file_details[0]["output_dir"]

    # Full data
    processed_file_details = process_csv(
        [latest_file_details],
        output_dir=datadir
    )

    processed_filename = processed_file_details[0]["processed_filename"]
    processed_dir = processed_file_details[0]["output_dir"]

    print(f"Finished processing {datadir}/{latest_file_details['filename']}, file is {processed_dir}/{processed_filename}")

    # process csv to update the non-public hospital table
    ingester.process_hospital(processed_dir, processed_filename, public=False)

    # process csv to update the public hospital table
    ingester.process_hospital(public_processed_dir, public_processed_filename)

    # process supplies
    ingester.process_supplies(processed_dir, processed_filename)

    ingester.process_county_summaries(processed_dir, processed_filename)
    print("Finished processing instantaneous tables.")

def process_historical(dry_run=False, datadir=None, make_historical_csv=False, verbose=False):

    if datadir is None:
        datadir = "/tmp"

    ingester = Ingester(dry_run, verbose=verbose)

    files_to_not_sftp = ingester.gis.get_already_processed_files("summary_table")
    file_details, all_filenames = ingester.get_files_from_sftp(target_dir=datadir, only_latest=False, filenames_to_ignore=files_to_not_sftp)

    if len(file_details) == 0:
        print("No new files to process for historical summary table data.")
    else:
        processed_file_details = process_csv(file_details, output_dir=datadir)
        processed_dir = processed_file_details[0]["output_dir"]
        ingester.process_summaries(processed_dir, processed_file_details, make_historical_csv=make_historical_csv)

    files_to_not_sftp = ingester.gis.get_already_processed_files("full_historical_table")

    if make_historical_csv:
        # setting files_to_not_sftp to an empty list ensures we rebuild the full historical table
        files_to_not_sftp = []

    file_details, all_filenames = ingester.get_files_from_sftp(target_dir=datadir, only_latest=False, filenames_to_ignore=files_to_not_sftp)
    if len(file_details) == 0:
        print("No new files to process for historical data.")
    else:
        processed_file_details = process_csv(file_details, output_dir=datadir)
        processed_dir = processed_file_details[0]["output_dir"]
        ingester.process_historical_hos(processed_dir, processed_file_details, make_historical_csv=make_historical_csv)


    print("Finished processing historical tables.")


def process_canary_features(dry_run=False, datadir=None, verbose=False):
    print("Processing canary features...")
    if datadir is None:
        datadir = "/tmp"

    ingester = Ingester(dry_run, verbose=verbose)
    agol_connection = AGOLConnection()
    ingester.set_gis(agol_connection)

    print("XXX not doing historical averages yet")
    historical_gis_item_id = "3b39827f6f804c33b9b1114b5aa1d6b6" # v4
    historical_averages_item_id = ""
    ingester.process_daily_hospital_averages(historical_gis_item_id, historical_averages_item_id)
    print("Finished canary features.")

def main(dry_run, datadir=None, make_historical_csv=False, verbose=False):
    #process_canary_features(dry_run=dry_run, datadir=datadir, verbose=verbose)
    process_instantaneous(dry_run=dry_run, datadir=datadir, verbose=verbose)
    process_historical(dry_run=dry_run, datadir=datadir, make_historical_csv=make_historical_csv, verbose=verbose)

def instantaneous_pubsub(event, context):
    print("Started instantaneous ingestion processing run")
    process_instantaneous()
    print("Finished instantaneous ingestion processing run")

def historical_pubsub(event, context):
    print("Started historical ingestion processing run")
    process_historical()
    print("Finished historical ingestion processing run")

if __name__== "__main__":
    make_historical_csv = False
    dry_run = False
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry_run", action="store_true")
    parser.add_argument("--dir")
    parser.add_argument("--make_historical_csv", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    if args.dry_run is not None:
        dry_run = True
    if args.make_historical_csv is not None:
        make_historical_csv = True
    print(f"dry_run: {dry_run}")
    main(dry_run, datadir=args.dir, make_historical_csv=make_historical_csv)
    # note that the cli argument is --quiet but from here on the argument passed around is "verbose"
    verbose = not args.quiet
    main(args.dry_run, datadir=args.dir, make_historical_csv=args.make_historical_csv, verbose=verbose)
