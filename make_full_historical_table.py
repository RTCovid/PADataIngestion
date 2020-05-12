#!/usr/bin/env python3
import os
import argparse

from agol_connection import AGOLConnection
from operators import process_csv
from ingester import Ingester


if __name__ == "__main__":

    ingester = Ingester(dry_run=True)
    agol_connection = AGOLConnection()
    ingester.set_gis(agol_connection)

    datadir = "data"

    file_details, all_filenames = ingester.get_files_from_sftp(target_dir=datadir, only_latest=False)

    processed_file_details = process_csv(file_details, output_dir=datadir, overwrite=False)

    ingester.process_historical_hos(datadir, processed_file_details, make_historical_csv=True)
