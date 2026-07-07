# -*- coding: utf-8 -*-

import os
import traceback

import arcpy

import config
from scripts.common import ensure_output_dirs, find_original_rasters


def run():

    print("")
    print("[1/6] Validating inputs...")

    ensure_output_dirs(config)

    problems = []
    notes = []

    required_directories = [
        ("Original NEP directory", config.ORIGINAL_NEP_DIR),
        ("Projected NEP directory", config.PROJECTED_NEP_DIR),
        ("Boundary directory", config.BOUNDARY_DIR)
    ]

    for label, path in required_directories:

        if not os.path.isdir(path):
            problems.append(
                "{0} not found: {1}".format(label, path)
            )

    if not arcpy.Exists(config.REFERENCE_RASTER):
        problems.append(
            "Reference raster not found: {0}".format(
                config.REFERENCE_RASTER
            )
        )

    for ua in config.UA_ORDER:

        boundary = config.BOUNDARIES[ua]

        if not arcpy.Exists(boundary):
            problems.append(
                "Boundary not found for {0}: {1}".format(
                    ua,
                    boundary
                )
            )

    for path in [
        config.INDUSTRIAL_EMISSIONS_CSV,
        config.SECTOR_REMAINING_EMISSIONS_CSV
    ]:

        if not os.path.exists(path):
            problems.append(
                "Package input CSV not found: {0}".format(path)
            )

    if os.path.isdir(config.ORIGINAL_NEP_DIR):

        originals = find_original_rasters(
            config.ORIGINAL_NEP_DIR,
            config.YEARS
        )

        missing_original = [
            year for year in config.YEARS
            if year not in originals
        ]

        if missing_original:
            notes.append(
                "Original rasters not found for years: {0}. "
                "This is acceptable only when the corresponding "
                "projected rasters already exist.".format(
                    missing_original
                )
            )

    projected_missing = []

    for year in config.YEARS:

        projected = os.path.join(
            config.PROJECTED_NEP_DIR,
            "NEP_{0}_Albers.tif".format(year)
        )

        if not arcpy.Exists(projected):
            projected_missing.append(year)

    if projected_missing:
        notes.append(
            "Projected rasters currently missing for years: {0}".format(
                projected_missing
            )
        )

    spatial_status = arcpy.CheckExtension("Spatial")

    if spatial_status != "Available":
        problems.append(
            "Spatial Analyst is not available: {0}".format(
                spatial_status
            )
        )

    report_path = os.path.join(
        config.OUTPUT_REPORT_DIR,
        "input_validation_report.txt"
    )

    report = open(report_path, "w")
    report.write("Input validation report\n")
    report.write("=======================\n\n")

    if problems:
        report.write("Problems:\n")
        for problem in problems:
            report.write("- {0}\n".format(problem))
    else:
        report.write("Problems:\n- none\n")

    report.write("\nNotes:\n")

    if notes:
        for note in notes:
            report.write("- {0}\n".format(note))
    else:
        report.write("- none\n")

    report.close()

    for note in notes:
        print("  NOTE: {0}".format(note))

    if problems:

        for problem in problems:
            print("  ERROR: {0}".format(problem))

        raise RuntimeError(
            "Input validation failed. See: {0}".format(
                report_path
            )
        )

    print("  Input validation passed.")
    print("  Report: {0}".format(report_path))


if __name__ == "__main__":

    try:
        run()
    except Exception:
        print(traceback.format_exc())
        raise
