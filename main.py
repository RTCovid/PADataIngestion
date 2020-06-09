#!/usr/bin/env python3
import os
import argparse
from datetime import datetime

from header_mapping import HeaderMapping
from operators import process_csv
from agol_connection import AGOLConnection
from validator import CSVValidator
from ingester import Ingester


def process_instantaneous(dry_run=False, datadir=None, verbose=False):

    hm_hos = HeaderMapping("HOS")

    start = datetime.now()
    print("\nSTARTING process_instantaneous()")

    if datadir is None:
        datadir = "/tmp"

    ingester = Ingester(dry_run, verbose=verbose)

    print("Getting latest HOS file from SFTP...")
    a = datetime.now()
    file_details, all_filenames = ingester.get_files_from_sftp(target_dir=datadir)
    print(f"Finished: {datetime.now() - a}")

    latest_file_details = file_details[0]

    # run a validation on the latest file (the one that will be used for instantaneous)
    a = datetime.now()
    v = CSVValidator("HOS")
    fpath = os.path.join(latest_file_details['dir'], latest_file_details['filename'])
    v.validate_csv(fpath)
    print(f"latest CSV validated: {datetime.now() - a}")

    # Public-only data
    a = datetime.now()
    public_processed_file_details = process_csv(
        [latest_file_details],
        output_prefix="public_processed_HOS_",
        columns_wanted=hm_hos.get_public_column_names(),
        output_dir=datadir,
    )
    public_processed_filename = public_processed_file_details[0]["processed_filename"]
    public_processed_dir = public_processed_file_details[0]["output_dir"]
    print(f"processed latest CSV (only public columns): {datetime.now() - a}")

    # Full data
    a = datetime.now()
    processed_file_details = process_csv(
        [latest_file_details],
        output_dir=datadir
    )
    print(f"processed latest CSV (full): {datetime.now() - a}")

    processed_filename = processed_file_details[0]["processed_filename"]
    processed_dir = processed_file_details[0]["output_dir"]

    print(f"Finished processing {datadir}/{latest_file_details['filename']}, file is {processed_dir}/{processed_filename}")

    # process csv to update the non-public hospital table
    a = datetime.now()
    ingester.process_hospital(processed_dir, processed_filename, public=False)
    print(f"process hospital (full): {datetime.now() - a}")

    # process csv to update the public hospital table
    a = datetime.now()
    ingester.process_hospital(public_processed_dir, public_processed_filename)
    print(f"process hospital (public): {datetime.now() - a}")

    # process supplies
    a = datetime.now()
    ingester.process_supplies(processed_dir, processed_filename)
    print(f"process supplies: {datetime.now() - a}")

    # process DHS feeding needs county summaries
    a = datetime.now()
    ingester.process_DHS_feeding_needs_county_summaries(datadir)
    print(f"process DHS feeding needs county summaries: {datetime.now() - a}")

    # process county-level summary
    a = datetime.now()
    ingester.process_county_summaries(processed_dir, processed_filename)
    print(f"process county summaries: {datetime.now() - a}")
    print(f"FINISHED process_instantaneous(): {datetime.now() - start}")

def process_historical(dry_run=False, datadir=None, make_historical_csv=False, verbose=False):

    print("\nSTARTING process_historical()")
    start = datetime.now()
    if datadir is None:
        datadir = "/tmp"

    ingester = Ingester(dry_run, verbose=verbose)

    a = datetime.now()
    files_to_not_sftp = ingester.get_already_processed_files("summary_table")
    print(f"determined already processed files (summary_table): {datetime.now() - a}")

    a = datetime.now()
    file_details, all_filenames = ingester.get_files_from_sftp(target_dir=datadir, only_latest=False, filenames_to_ignore=files_to_not_sftp)
    print(f"downloaded files: {datetime.now() - a}")

    if len(file_details) == 0:
        print("  No new files to process for historical summary table data.")
    else:
        a = datetime.now()
        processed_file_details = process_csv(file_details, output_dir=datadir)
        print(f"process_csv(): {datetime.now() - a}")
        processed_dir = processed_file_details[0]["output_dir"]
        a = datetime.now()
        ingester.process_summaries(processed_dir, processed_file_details, make_historical_csv=make_historical_csv)
        print(f"process_summaries(): {datetime.now() - a}")

    a = datetime.now()
    files_to_not_sftp = ingester.get_already_processed_files("full_historical_table")
    print(f"determined already processed files (full_historical_table): {datetime.now() - a}")

    if make_historical_csv:
        # setting files_to_not_sftp to an empty list ensures we rebuild the full historical table
        files_to_not_sftp = []

    a = datetime.now()
    file_details, all_filenames = ingester.get_files_from_sftp(target_dir=datadir, only_latest=False, filenames_to_ignore=files_to_not_sftp)
    print(f"downloaded files: {datetime.now() - a}")

    if len(file_details) == 0:
        print("  No new files to process for historical data.")
    else:
        lf = len(file_details)
        print(f"  {lf} new files to process for historical data.")
        a = datetime.now()
        processed_file_details = process_csv(file_details, output_dir=datadir)
        print(f"process_csv(): {datetime.now() - a}")
        processed_dir = processed_file_details[0]["output_dir"]
        a = datetime.now()
        ingester.process_historical_hos(processed_dir, processed_file_details, make_historical_csv=make_historical_csv)
        print(f"process_historical_hos: {datetime.now() - a}")

    print(f"FINISHED process_historical(): {datetime.now()-start}")


def process_canary_features(dry_run=False, datadir=None, verbose=False):
    print("Processing canary features...")
    if datadir is None:
        datadir = "/tmp"

    ingester = Ingester(dry_run, verbose=verbose)

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

    print(f"dry_run: {args.dry_run}")

    # note that the cli argument is --quiet but from here on the argument passed around is "verbose"
    verbose = not args.quiet
    main(args.dry_run, datadir=args.dir, make_historical_csv=args.make_historical_csv, verbose=verbose)
