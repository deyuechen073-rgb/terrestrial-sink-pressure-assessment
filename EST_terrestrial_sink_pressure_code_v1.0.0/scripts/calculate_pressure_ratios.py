# -*- coding: utf-8 -*-

import os
import csv
import traceback

import config
from scripts.common import read_csv_dicts


def run():

    print("")
    print("[4/6] Calculating industrial emission pressure ratios...")

    main_results_path = os.path.join(
        config.OUTPUT_TABLE_DIR,
        "main_results_ge10.csv"
    )

    sensitivity_path = os.path.join(
        config.OUTPUT_TABLE_DIR,
        "sensitivity_ge5_ge10_ge15.csv"
    )

    coverage_path = os.path.join(
        config.OUTPUT_TABLE_DIR,
        "threshold_coverage_1_20.csv"
    )

    for path in [
        main_results_path,
        sensitivity_path,
        coverage_path
    ]:

        if not os.path.exists(path):
            raise RuntimeError(
                "Required result file not found: {0}".format(path)
            )

    emissions_rows = read_csv_dicts(
        config.INDUSTRIAL_EMISSIONS_CSV
    )
    sector_rows = read_csv_dicts(
        config.SECTOR_REMAINING_EMISSIONS_CSV
    )
    main_rows = read_csv_dicts(main_results_path)
    sensitivity_rows = read_csv_dicts(sensitivity_path)

    emissions = {}

    for row in emissions_rows:
        emissions[row["UA"]] = float(
            row["Reported_Remaining_Industrial_Emissions_MtCO2_yr"]
        )

    main_sink = {}

    for row in main_rows:
        main_sink[row["UA"]] = float(
            row["Terrestrial_Sink_MtCO2_yr"]
        )

    sensitivity = {}

    for row in sensitivity_rows:

        sensitivity[row["UA"]] = {
            5: float(row["Sink_ge5_MtCO2_yr"]),
            10: float(row["Sink_ge10_MtCO2_yr"]),
            15: float(row["Sink_ge15_MtCO2_yr"])
        }

    # Validate sector totals against reported manuscript totals.
    sector_totals = {}
    chemical_values = {}

    for row in sector_rows:

        ua = row["UA"]
        sector = row["Subsector"]
        value = float(row["Remaining_Emissions_MtCO2_yr"])

        sector_totals[ua] = sector_totals.get(ua, 0.0) + value

        if sector == "Chemicals":
            chemical_values[ua] = value

    sector_summary_path = os.path.join(
        config.OUTPUT_TABLE_DIR,
        "sector_remaining_emissions_summary.csv"
    )

    handle = open(sector_summary_path, "wb")
    writer = csv.writer(handle)

    writer.writerow([
        "UA",
        "Exact_Sector_Sum_MtCO2_yr",
        "Reported_Total_MtCO2_yr",
        "Difference_MtCO2_yr",
        "Chemical_Emissions_MtCO2_yr",
        "Chemical_Share_pct"
    ])

    for ua in config.UA_ORDER:

        exact_total = sector_totals[ua]
        reported_total = emissions[ua]
        chemical_value = chemical_values[ua]

        writer.writerow([
            ua,
            exact_total,
            reported_total,
            exact_total - reported_total,
            chemical_value,
            chemical_value / exact_total * 100.0
        ])

    handle.close()

    # Temporal completeness threshold sensitivity.
    temporal_output = os.path.join(
        config.OUTPUT_TABLE_DIR,
        "pressure_ratio_temporal_thresholds.csv"
    )

    handle = open(temporal_output, "wb")
    writer = csv.writer(handle)

    writer.writerow([
        "UA",
        "Minimum_Valid_Years",
        "Remaining_Industrial_Emissions_MtCO2_yr",
        "Terrestrial_Sink_MtCO2_yr",
        "Emission_to_Sink_Pressure_Ratio"
    ])

    for ua in config.UA_ORDER:

        for threshold in config.TEMPORAL_THRESHOLDS:

            sink_value = sensitivity[ua][threshold]
            ratio = emissions[ua] / sink_value

            writer.writerow([
                ua,
                threshold,
                emissions[ua],
                sink_value,
                ratio
            ])

    handle.close()

    # Alternative benchmark-level sensitivity.
    benchmark_output = os.path.join(
        config.OUTPUT_TABLE_DIR,
        "sink_capacity_sensitivity_80_100_120.csv"
    )

    handle = open(benchmark_output, "wb")
    writer = csv.writer(handle)

    writer.writerow([
        "UA",
        "Sink_Capacity_Scale",
        "Sink_Capacity_Percent",
        "Remaining_Industrial_Emissions_MtCO2_yr",
        "Historical_Terrestrial_Sink_MtCO2_yr",
        "Adjusted_Terrestrial_Sink_MtCO2_yr",
        "Emission_to_Sink_Pressure_Ratio"
    ])

    for ua in config.UA_ORDER:

        for scale in config.SINK_CAPACITY_SCALES:

            adjusted_sink = main_sink[ua] * scale
            ratio = emissions[ua] / adjusted_sink

            writer.writerow([
                ua,
                scale,
                int(round(scale * 100.0)),
                emissions[ua],
                main_sink[ua],
                adjusted_sink,
                ratio
            ])

    handle.close()

    summary_output = os.path.join(
        config.OUTPUT_TABLE_DIR,
        "source_sink_coupling_summary.csv"
    )

    handle = open(summary_output, "wb")
    writer = csv.writer(handle)

    writer.writerow([
        "UA",
        "Remaining_Industrial_Emissions_MtCO2_yr",
        "Main_Terrestrial_Sink_MtCO2_yr",
        "Main_Pressure_Ratio",
        "Temporal_Sink_Min_MtCO2_yr",
        "Temporal_Sink_Max_MtCO2_yr",
        "Temporal_Pressure_Ratio_Min",
        "Temporal_Pressure_Ratio_Max",
        "Benchmark_Pressure_Ratio_80pct",
        "Benchmark_Pressure_Ratio_100pct",
        "Benchmark_Pressure_Ratio_120pct",
        "Interpretation_Note"
    ])

    for ua in config.UA_ORDER:

        sink_values = [
            sensitivity[ua][5],
            sensitivity[ua][10],
            sensitivity[ua][15]
        ]

        min_sink = min(sink_values)
        max_sink = max(sink_values)

        ratio_main = emissions[ua] / main_sink[ua]

        note = (
            "Relative magnitude indicator only; it does not allocate "
            "regional ecosystem sinks to industry and does not represent "
            "a local offset obligation or industrial net-zero feasibility."
        )

        writer.writerow([
            ua,
            emissions[ua],
            main_sink[ua],
            ratio_main,
            min_sink,
            max_sink,
            emissions[ua] / max_sink,
            emissions[ua] / min_sink,
            emissions[ua] / (main_sink[ua] * 0.8),
            emissions[ua] / main_sink[ua],
            emissions[ua] / (main_sink[ua] * 1.2),
            note
        ])

    handle.close()

    print("  Pressure-ratio calculations completed.")
    print("  Temporal sensitivity: {0}".format(temporal_output))
    print("  Benchmark sensitivity: {0}".format(benchmark_output))


if __name__ == "__main__":

    try:
        run()
    except Exception:
        print(traceback.format_exc())
        raise
