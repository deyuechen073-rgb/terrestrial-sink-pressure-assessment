# -*- coding: utf-8 -*-

import os
import re
import csv


def ensure_dir(path):

    if not os.path.exists(path):
        os.makedirs(path)


def ensure_output_dirs(config):

    paths = [
        config.OUTPUT_ROOT,
        config.OUTPUT_RASTER_DIR,
        config.OUTPUT_TABLE_DIR,
        config.OUTPUT_FIGURE_DATA_DIR,
        config.OUTPUT_REPORT_DIR,
        config.TEMP_DIR
    ]

    for path in paths:
        ensure_dir(path)


def find_original_rasters(original_dir, years):

    year_to_raster = {}

    for filename in os.listdir(original_dir):

        lower_name = filename.lower()

        if not lower_name.endswith((".tif", ".tiff")):
            continue

        matches = re.findall(r"(20\d{2})", filename)

        if not matches:
            continue

        year = int(matches[-1])

        if year not in years:
            continue

        path = os.path.join(original_dir, filename)

        if year in year_to_raster:
            raise RuntimeError(
                "Multiple original rasters found for year {0}: "
                "{1} and {2}".format(
                    year,
                    year_to_raster[year],
                    path
                )
            )

        year_to_raster[year] = path

    return year_to_raster


def read_csv_dicts(path):

    rows = []

    handle = open(path, "rb")
    reader = csv.DictReader(handle)

    for row in reader:
        rows.append(row)

    handle.close()

    return rows


def write_csv(path, header, rows):

    handle = open(path, "wb")
    writer = csv.writer(handle)
    writer.writerow(header)

    for row in rows:
        writer.writerow(row)

    handle.close()


def float_or_none(value):

    if value in [None, ""]:
        return None

    return float(value)
