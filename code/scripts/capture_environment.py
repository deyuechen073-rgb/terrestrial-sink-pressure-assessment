# -*- coding: utf-8 -*-

import os
import sys
import platform
import datetime
import traceback

import numpy
import arcpy

import config
from scripts.common import ensure_output_dirs


def run():

    print("")
    print("[6/6] Capturing software environment...")

    ensure_output_dirs(config)

    output_path = os.path.join(
        config.OUTPUT_REPORT_DIR,
        "environment_details.txt"
    )

    install_info = arcpy.GetInstallInfo()

    handle = open(output_path, "w")

    handle.write("Software environment\n")
    handle.write("====================\n\n")
    handle.write(
        "Timestamp: {0}\n".format(
            datetime.datetime.now().isoformat()
        )
    )
    handle.write(
        "Operating system: {0}\n".format(
            platform.platform()
        )
    )
    handle.write(
        "Python version: {0}\n".format(
            sys.version.replace("\n", " ")
        )
    )
    handle.write(
        "NumPy version: {0}\n".format(
            numpy.__version__
        )
    )
    handle.write(
        "ArcGIS product: {0}\n".format(
            install_info.get("ProductName", "")
        )
    )
    handle.write(
        "ArcGIS version: {0}\n".format(
            install_info.get("Version", "")
        )
    )
    handle.write(
        "ArcGIS build: {0}\n".format(
            install_info.get("BuildNumber", "")
        )
    )
    handle.write(
        "Spatial Analyst status: {0}\n".format(
            arcpy.CheckExtension("Spatial")
        )
    )
    handle.write(
        "Project root: {0}\n".format(
            config.PROJECT_ROOT
        )
    )
    handle.write(
        "Reference raster: {0}\n".format(
            config.REFERENCE_RASTER
        )
    )

    handle.close()

    print("  Environment report: {0}".format(output_path))


if __name__ == "__main__":

    try:
        run()
    except Exception:
        print(traceback.format_exc())
        raise
