# -*- coding: utf-8 -*-

import os
import csv
import traceback

import config
from scripts.common import read_csv_dicts


def _assert_close(
    label,
    actual,
    expected,
    tolerance,
    failures
):

    difference = abs(actual - expected)

    if difference > tolerance:
        failures.append(
            "{0}: actual={1}, expected={2}, "
            "difference={3}, tolerance={4}".format(
                label,
                actual,
                expected,
                difference,
                tolerance
            )
        )


def run():

    print("")
    print("Validating outputs against expected results...")

    actual_main_path = os.path.join(
        config.OUTPUT_TABLE_DIR,
        "main_results_ge10.csv"
    )

    actual_sensitivity_path = os.path.join(
        config.OUTPUT_TABLE_DIR,
        "sensitivity_ge5_ge10_ge15.csv"
    )

    if not os.path.exists(actual_main_path):
        raise RuntimeError(
            "Actual main result file not found: {0}".format(
                actual_main_path
            )
        )

    if not os.path.exists(actual_sensitivity_path):
        raise RuntimeError(
            "Actual sensitivity file not found: {0}".format(
                actual_sensitivity_path
            )
        )

    actual_main = {}
    expected_main = {}

    for row in read_csv_dicts(actual_main_path):
        actual_main[row["UA"]] = row

    for row in read_csv_dicts(config.EXPECTED_MAIN_RESULTS_CSV):
        expected_main[row["UA"]] = row

    actual_sensitivity = {}
    expected_sensitivity = {}

    for row in read_csv_dicts(actual_sensitivity_path):
        actual_sensitivity[row["UA"]] = row

    for row in read_csv_dicts(
        config.EXPECTED_TEMPORAL_SENSITIVITY_CSV
    ):
        expected_sensitivity[row["UA"]] = row

    failures = []

    for ua in config.UA_ORDER:

        _assert_close(
            "{0} selected area".format(ua),
            float(actual_main[ua]["Selected_Area_km2"]),
            float(expected_main[ua]["Selected_Area_km2"]),
            config.AREA_ABS_TOLERANCE_KM2,
            failures
        )

        _assert_close(
            "{0} coverage".format(ua),
            float(
                actual_main[ua][
                    "Coverage_vs_EverValid_pct"
                ]
            ),
            float(
                expected_main[ua][
                    "Coverage_vs_EverValid_pct"
                ]
            ),
            config.COVERAGE_ABS_TOLERANCE_PCT,
            failures
        )

        _assert_close(
            "{0} mean NEP".format(ua),
            float(actual_main[ua]["Mean_NEP_gC_m2_yr"]),
            float(expected_main[ua]["Mean_NEP_gC_m2_yr"]),
            config.MEAN_NEP_ABS_TOLERANCE,
            failures
        )

        _assert_close(
            "{0} main sink".format(ua),
            float(
                actual_main[ua][
                    "Terrestrial_Sink_MtCO2_yr"
                ]
            ),
            float(
                expected_main[ua][
                    "Terrestrial_Sink_MtCO2_yr"
                ]
            ),
            config.SINK_ABS_TOLERANCE_MTCO2_YR,
            failures
        )

        for field in [
            "Sink_ge5_MtCO2_yr",
            "Sink_ge10_MtCO2_yr",
            "Sink_ge15_MtCO2_yr"
        ]:

            _assert_close(
                "{0} {1}".format(ua, field),
                float(actual_sensitivity[ua][field]),
                float(expected_sensitivity[ua][field]),
                config.SINK_ABS_TOLERANCE_MTCO2_YR,
                failures
            )

    report_path = os.path.join(
        config.OUTPUT_REPORT_DIR,
        "expected_result_validation.txt"
    )

    handle = open(report_path, "w")
    handle.write("Expected-result validation\n")
    handle.write("==========================\n\n")

    if failures:

        handle.write("Status: FAILED\n\n")

        for failure in failures:
            handle.write("- {0}\n".format(failure))

    else:

        handle.write("Status: PASSED\n")
        handle.write(
            "All main and temporal-sensitivity results "
            "match the archived expected values within "
            "the configured tolerances.\n"
        )

    handle.close()

    if failures:
        raise RuntimeError(
            "Expected-result validation failed. See: {0}".format(
                report_path
            )
        )

    print("  Expected-result validation passed.")
    print("  Report: {0}".format(report_path))


if __name__ == "__main__":

    try:
        run()
    except Exception:
        print(traceback.format_exc())
        raise
