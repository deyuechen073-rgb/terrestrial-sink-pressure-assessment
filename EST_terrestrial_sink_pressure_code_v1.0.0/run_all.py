# -*- coding: utf-8 -*-

import os
import sys
import traceback

PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))

if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, PACKAGE_ROOT)

import config
from scripts import validate_inputs
from scripts import project_nep_rasters
from scripts import calculate_terrestrial_sink
from scripts import calculate_pressure_ratios
from scripts import build_manuscript_outputs
from scripts import capture_environment


def main():

    print("")
    print("======================================================")
    print("Terrestrial sink benchmark and industrial pressure")
    print("Reproducible analysis pipeline")
    print("======================================================")

    validate_inputs.run()

    if config.RUN_PROJECTION_STEP:
        project_nep_rasters.run()

    calculate_terrestrial_sink.run()
    calculate_pressure_ratios.run()
    build_manuscript_outputs.run()
    capture_environment.run()

    if config.RUN_EXPECTED_RESULT_CHECK:
        from tests import validate_expected_results
        validate_expected_results.run()

    print("")
    print("======================================================")
    print("PIPELINE COMPLETED")
    print("Outputs:")
    print(config.OUTPUT_ROOT)
    print("======================================================")


if __name__ == "__main__":

    try:
        main()
    except Exception:
        print("")
        print("PIPELINE FAILED")
        print(traceback.format_exc())
        raise
