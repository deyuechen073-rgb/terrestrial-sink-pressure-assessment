# -*- coding: utf-8 -*-

import os
import csv
import traceback

import arcpy
import numpy as np

from arcpy.sa import CreateConstantRaster, ExtractByMask

import config
from scripts.common import ensure_output_dirs


def _save_array_as_raster(
    array_data,
    output_path,
    lower_left,
    cell_x,
    cell_y,
    nodata_value
):

    if arcpy.Exists(output_path):
        arcpy.Delete_management(output_path)

    raster = arcpy.NumPyArrayToRaster(
        array_data,
        lower_left,
        cell_x,
        cell_y,
        nodata_value
    )

    raster.save(output_path)
    arcpy.CalculateStatistics_management(output_path)


def _create_zone_raster(ua, boundary, reference_raster):

    output_path = os.path.join(
        config.TEMP_DIR,
        "{0}_zone.tif".format(ua)
    )

    if arcpy.Exists(output_path):
        arcpy.Delete_management(output_path)

    boundary_extent = arcpy.Describe(boundary).extent

    arcpy.env.snapRaster = reference_raster
    arcpy.env.cellSize = reference_raster
    arcpy.env.extent = boundary_extent
    arcpy.env.mask = boundary

    constant = CreateConstantRaster(
        1,
        "INTEGER",
        config.TARGET_CELL_SIZE_M,
        boundary_extent
    )

    zone = ExtractByMask(constant, boundary)
    zone.save(output_path)

    return output_path


def run():

    print("")
    print("[3/6] Calculating terrestrial ecosystem sink benchmarks...")

    ensure_output_dirs(config)

    if arcpy.CheckExtension("Spatial") != "Available":
        raise RuntimeError("Spatial Analyst is not available.")

    arcpy.CheckOutExtension("Spatial")

    try:

        arcpy.env.overwriteOutput = (
            config.OVERWRITE_ANALYSIS_OUTPUTS
        )

        reference_desc = arcpy.Describe(
            config.REFERENCE_RASTER
        )

        reference_sr = reference_desc.spatialReference

        cell_x = abs(float(
            arcpy.GetRasterProperties_management(
                config.REFERENCE_RASTER,
                "CELLSIZEX"
            ).getOutput(0)
        ))

        cell_y = abs(float(
            arcpy.GetRasterProperties_management(
                config.REFERENCE_RASTER,
                "CELLSIZEY"
            ).getOutput(0)
        ))

        cell_area_m2 = cell_x * cell_y
        cell_area_km2 = cell_area_m2 / 1000000.0

        # g C m-2 yr-1 × m2 × 44/12 × 10-12
        sink_factor = (
            cell_area_m2
            * (44.0 / 12.0)
            * 1.0e-12
        )

        summary_rows = []
        coverage_rows = []

        for ua in config.UA_ORDER:

            print("")
            print("  Processing {0}...".format(ua))

            boundary = config.BOUNDARIES[ua]
            arcpy.env.outputCoordinateSystem = reference_sr

            zone_raster = _create_zone_raster(
                ua,
                boundary,
                config.REFERENCE_RASTER
            )

            zone_desc = arcpy.Describe(zone_raster)
            zone_extent = zone_desc.extent

            rows = int(
                arcpy.GetRasterProperties_management(
                    zone_raster,
                    "ROWCOUNT"
                ).getOutput(0)
            )

            columns = int(
                arcpy.GetRasterProperties_management(
                    zone_raster,
                    "COLUMNCOUNT"
                ).getOutput(0)
            )

            zone_array = arcpy.RasterToNumPyArray(
                zone_raster,
                nodata_to_value=0
            ).astype(np.int8)

            zone_mask = zone_array == 1

            valid_year_count = np.zeros(
                (rows, columns),
                dtype=np.int16
            )

            nep_sum = np.zeros(
                (rows, columns),
                dtype=np.float64
            )

            lower_left = arcpy.Point(
                zone_extent.XMin,
                zone_extent.YMin
            )

            for year in config.YEARS:

                print("    Reading {0}...".format(year))

                raster_path = os.path.join(
                    config.PROJECTED_NEP_DIR,
                    "NEP_{0}_Albers.tif".format(year)
                )

                if not arcpy.Exists(raster_path):
                    raise RuntimeError(
                        "Projected raster not found: {0}".format(
                            raster_path
                        )
                    )

                array_data = arcpy.RasterToNumPyArray(
                    raster_path,
                    lower_left,
                    columns,
                    rows,
                    nodata_to_value=-1.0e30
                ).astype(np.float64)

                valid = (
                    zone_mask
                    & np.isfinite(array_data)
                    & (array_data > config.VALID_NEP_MIN)
                    & (array_data < config.VALID_NEP_MAX)
                )

                valid_year_count[valid] += 1
                nep_sum[valid] += array_data[valid]

                del array_data
                del valid

            # Save valid-observation-year raster.
            count_output = np.empty(
                (rows, columns),
                dtype=np.int16
            )
            count_output.fill(-9999)
            count_output[zone_mask] = (
                valid_year_count[zone_mask]
            )

            count_raster_path = os.path.join(
                config.OUTPUT_RASTER_DIR,
                "{0}_valid_year_count_2001_2020.tif".format(
                    ua
                )
            )

            _save_array_as_raster(
                count_output,
                count_raster_path,
                lower_left,
                cell_x,
                cell_y,
                -9999
            )

            boundary_pixels = int(
                np.count_nonzero(zone_mask)
            )

            ever_valid_mask = (
                zone_mask
                & (valid_year_count >= 1)
            )

            ever_valid_pixels = int(
                np.count_nonzero(ever_valid_mask)
            )

            # Coverage response for all thresholds from 1 to 20 years.
            for threshold in config.ALL_COVERAGE_THRESHOLDS:

                selected = (
                    zone_mask
                    & (valid_year_count >= threshold)
                )

                selected_pixels = int(
                    np.count_nonzero(selected)
                )

                coverage_boundary = (
                    selected_pixels
                    / float(boundary_pixels)
                    * 100.0
                ) if boundary_pixels > 0 else 0.0

                coverage_ever = (
                    selected_pixels
                    / float(ever_valid_pixels)
                    * 100.0
                ) if ever_valid_pixels > 0 else 0.0

                coverage_rows.append([
                    ua,
                    threshold,
                    boundary_pixels,
                    boundary_pixels * cell_area_km2,
                    ever_valid_pixels,
                    ever_valid_pixels * cell_area_km2,
                    selected_pixels,
                    selected_pixels * cell_area_km2,
                    coverage_boundary,
                    coverage_ever
                ])

            # Main and sensitivity thresholds.
            for threshold in config.TEMPORAL_THRESHOLDS:

                selected = (
                    zone_mask
                    & (valid_year_count >= threshold)
                )

                selected_pixels = int(
                    np.count_nonzero(selected)
                )

                if selected_pixels == 0:
                    raise RuntimeError(
                        "No selected pixels for {0}, threshold {1}".format(
                            ua,
                            threshold
                        )
                    )

                mean_values = (
                    nep_sum[selected]
                    / valid_year_count[selected].astype(np.float64)
                )

                mean_nep = float(
                    mean_values.mean(dtype=np.float64)
                )

                sum_pixel_mean_nep = float(
                    mean_values.sum(dtype=np.float64)
                )

                sink_mtco2_yr = (
                    sum_pixel_mean_nep
                    * sink_factor
                )

                coverage_ever = (
                    selected_pixels
                    / float(ever_valid_pixels)
                    * 100.0
                )

                mean_output = np.empty(
                    (rows, columns),
                    dtype=np.float32
                )
                mean_output.fill(-9999.0)
                mean_output[selected] = (
                    mean_values.astype(np.float32)
                )

                mean_raster_path = os.path.join(
                    config.OUTPUT_RASTER_DIR,
                    "{0}_NEP_longterm_mean_ge{1}.tif".format(
                        ua,
                        threshold
                    )
                )

                _save_array_as_raster(
                    mean_output,
                    mean_raster_path,
                    lower_left,
                    cell_x,
                    cell_y,
                    -9999.0
                )

                summary_rows.append([
                    ua,
                    threshold,
                    boundary_pixels,
                    boundary_pixels * cell_area_km2,
                    ever_valid_pixels,
                    ever_valid_pixels * cell_area_km2,
                    selected_pixels,
                    selected_pixels * cell_area_km2,
                    coverage_ever,
                    mean_nep,
                    sum_pixel_mean_nep,
                    sink_mtco2_yr,
                    mean_raster_path
                ])

                print(
                    "    >= {0} years: {1:.6f} Mt CO2 yr-1".format(
                        threshold,
                        sink_mtco2_yr
                    )
                )

                del selected
                del mean_values
                del mean_output

            del zone_array
            del zone_mask
            del valid_year_count
            del nep_sum
            del count_output

            arcpy.ClearWorkspaceCache_management()

        coverage_csv = os.path.join(
            config.OUTPUT_TABLE_DIR,
            "threshold_coverage_1_20.csv"
        )

        handle = open(coverage_csv, "wb")
        writer = csv.writer(handle)

        writer.writerow([
            "UA",
            "Minimum_Valid_Years",
            "Boundary_Pixels",
            "Boundary_Area_km2",
            "Ever_Valid_Pixels",
            "Ever_Valid_Area_km2",
            "Selected_Pixels",
            "Selected_Area_km2",
            "Coverage_vs_Boundary_pct",
            "Coverage_vs_EverValid_pct"
        ])

        for row in coverage_rows:
            writer.writerow(row)

        handle.close()

        summary_csv = os.path.join(
            config.OUTPUT_TABLE_DIR,
            "long_term_sink_summary.csv"
        )

        handle = open(summary_csv, "wb")
        writer = csv.writer(handle)

        writer.writerow([
            "UA",
            "Minimum_Valid_Years",
            "Boundary_Pixels",
            "Boundary_Area_km2",
            "Ever_Valid_Pixels",
            "Ever_Valid_Area_km2",
            "Selected_Pixels",
            "Selected_Area_km2",
            "Coverage_vs_EverValid_pct",
            "Mean_NEP_gC_m2_yr",
            "Sum_Pixel_Mean_NEP",
            "Sink_MtCO2_yr",
            "Mean_NEP_Raster"
        ])

        for row in summary_rows:
            writer.writerow(row)

        handle.close()

        main_csv = os.path.join(
            config.OUTPUT_TABLE_DIR,
            "main_results_ge10.csv"
        )

        handle = open(main_csv, "wb")
        writer = csv.writer(handle)

        writer.writerow([
            "UA",
            "Minimum_Valid_Years",
            "Selected_Area_km2",
            "Coverage_vs_EverValid_pct",
            "Mean_NEP_gC_m2_yr",
            "Terrestrial_Sink_MtCO2_yr"
        ])

        for row in summary_rows:

            if int(row[1]) == int(config.MAIN_THRESHOLD):

                writer.writerow([
                    row[0],
                    row[1],
                    row[7],
                    row[8],
                    row[9],
                    row[11]
                ])

        handle.close()

        sink_lookup = {}

        for row in summary_rows:
            sink_lookup[(row[0], int(row[1]))] = float(row[11])

        sensitivity_csv = os.path.join(
            config.OUTPUT_TABLE_DIR,
            "sensitivity_ge5_ge10_ge15.csv"
        )

        handle = open(sensitivity_csv, "wb")
        writer = csv.writer(handle)

        writer.writerow([
            "UA",
            "Sink_ge5_MtCO2_yr",
            "Sink_ge10_MtCO2_yr",
            "Sink_ge15_MtCO2_yr",
            "ge5_vs_ge10_pct",
            "ge15_vs_ge10_pct"
        ])

        for ua in config.UA_ORDER:

            sink5 = sink_lookup[(ua, 5)]
            sink10 = sink_lookup[(ua, 10)]
            sink15 = sink_lookup[(ua, 15)]

            writer.writerow([
                ua,
                sink5,
                sink10,
                sink15,
                (sink5 - sink10) / sink10 * 100.0,
                (sink15 - sink10) / sink10 * 100.0
            ])

        handle.close()

        print("  Terrestrial sink calculation completed.")
        print("  Main results: {0}".format(main_csv))
        print("  Sensitivity: {0}".format(sensitivity_csv))

    finally:

        arcpy.env.snapRaster = None
        arcpy.env.cellSize = None
        arcpy.env.extent = None
        arcpy.env.mask = None
        arcpy.env.outputCoordinateSystem = None

        arcpy.CheckInExtension("Spatial")


if __name__ == "__main__":

    try:
        run()
    except Exception:
        print(traceback.format_exc())
        raise
