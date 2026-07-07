# -*- coding: utf-8 -*-

import os
import traceback

import arcpy

import config
from scripts.common import ensure_output_dirs, find_original_rasters


def run():

    print("")
    print("[2/6] Projecting and aligning annual NEP rasters...")

    ensure_output_dirs(config)

    if not arcpy.Exists(config.REFERENCE_RASTER):
        raise RuntimeError(
            "The aligned 2001 reference raster is required: {0}".format(
                config.REFERENCE_RASTER
            )
        )

    original_rasters = find_original_rasters(
        config.ORIGINAL_NEP_DIR,
        config.YEARS
    )

    reference_desc = arcpy.Describe(
        config.REFERENCE_RASTER
    )

    reference_sr = reference_desc.spatialReference

    arcpy.env.overwriteOutput = (
        config.OVERWRITE_PROJECTED_RASTERS
    )
    arcpy.env.snapRaster = config.REFERENCE_RASTER
    arcpy.env.cellSize = config.REFERENCE_RASTER
    arcpy.env.extent = config.REFERENCE_RASTER
    arcpy.env.outputCoordinateSystem = reference_sr

    try:

        for year in config.YEARS:

            output_raster = os.path.join(
                config.PROJECTED_NEP_DIR,
                "NEP_{0}_Albers.tif".format(year)
            )

            if arcpy.Exists(output_raster):

                if not config.OVERWRITE_PROJECTED_RASTERS:
                    print(
                        "  Skipping existing raster for {0}".format(
                            year
                        )
                    )
                    continue

                if year == config.YEAR_START:
                    print(
                        "  Keeping the 2001 reference raster."
                    )
                    continue

                arcpy.Delete_management(output_raster)

            if year not in original_rasters:
                raise RuntimeError(
                    "No original raster available for year {0}".format(
                        year
                    )
                )

            print("  Projecting {0}...".format(year))

            arcpy.ProjectRaster_management(
                original_rasters[year],
                output_raster,
                reference_sr,
                config.RESAMPLING_METHOD,
                config.TARGET_CELL_SIZE_M
            )

    finally:

        arcpy.env.snapRaster = None
        arcpy.env.cellSize = None
        arcpy.env.extent = None
        arcpy.env.outputCoordinateSystem = None

    print("  Projection and alignment completed.")


if __name__ == "__main__":

    try:
        run()
    except Exception:
        print(traceback.format_exc())
        raise
