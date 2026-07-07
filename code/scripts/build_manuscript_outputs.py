# -*- coding: utf-8 -*-

import os
import csv
import traceback

import config
from scripts.common import read_csv_dicts


def _lookup_coverage(coverage_rows):

    lookup = {}

    for row in coverage_rows:

        key = (
            row["UA"],
            int(row["Minimum_Valid_Years"])
        )

        lookup[key] = float(
            row["Coverage_vs_EverValid_pct"]
        )

    return lookup


def run():

    print("")
    print("[5/6] Building manuscript-ready tables and figure data...")

    main_rows = read_csv_dicts(
        os.path.join(
            config.OUTPUT_TABLE_DIR,
            "main_results_ge10.csv"
        )
    )

    temporal_rows = read_csv_dicts(
        os.path.join(
            config.OUTPUT_TABLE_DIR,
            "pressure_ratio_temporal_thresholds.csv"
        )
    )

    benchmark_rows = read_csv_dicts(
        os.path.join(
            config.OUTPUT_TABLE_DIR,
            "sink_capacity_sensitivity_80_100_120.csv"
        )
    )

    coverage_rows = read_csv_dicts(
        os.path.join(
            config.OUTPUT_TABLE_DIR,
            "threshold_coverage_1_20.csv"
        )
    )

    emissions_rows = read_csv_dicts(
        config.INDUSTRIAL_EMISSIONS_CSV
    )

    sector_rows = read_csv_dicts(
        config.SECTOR_REMAINING_EMISSIONS_CSV
    )

    emissions = {}
    for row in emissions_rows:
        emissions[row["UA"]] = float(
            row["Reported_Remaining_Industrial_Emissions_MtCO2_yr"]
        )

    sink = {}
    for row in main_rows:
        sink[row["UA"]] = float(
            row["Terrestrial_Sink_MtCO2_yr"]
        )

    temporal = {}
    for row in temporal_rows:
        temporal[
            (
                row["UA"],
                int(row["Minimum_Valid_Years"])
            )
        ] = {
            "sink": float(row["Terrestrial_Sink_MtCO2_yr"]),
            "ratio": float(row["Emission_to_Sink_Pressure_Ratio"])
        }

    benchmark = {}
    for row in benchmark_rows:
        benchmark[
            (
                row["UA"],
                int(row["Sink_Capacity_Percent"])
            )
        ] = {
            "adjusted_sink": float(
                row["Adjusted_Terrestrial_Sink_MtCO2_yr"]
            ),
            "ratio": float(
                row["Emission_to_Sink_Pressure_Ratio"]
            )
        }

    coverage = _lookup_coverage(coverage_rows)

    # Main-text Table 1.
    table1_path = os.path.join(
        config.OUTPUT_TABLE_DIR,
        "Table1_main_text.csv"
    )

    handle = open(table1_path, "wb")
    writer = csv.writer(handle)

    writer.writerow([
        "UA",
        "2060_remaining_industrial_emissions_MtCO2_yr",
        "Historical_terrestrial_sink_benchmark_MtCO2_yr",
        "Baseline_pressure_ratio",
        "Pressure_ratio_range_under_80_120pct_benchmarks"
    ])

    for ua in config.UA_ORDER:

        ratio80 = benchmark[(ua, 80)]["ratio"]
        ratio120 = benchmark[(ua, 120)]["ratio"]

        writer.writerow([
            ua,
            emissions[ua],
            sink[ua],
            emissions[ua] / sink[ua],
            "{0:.2f}-{1:.2f}".format(
                min(ratio80, ratio120),
                max(ratio80, ratio120)
            )
        ])

    handle.close()

    # Supporting Information Table S9 Panel A.
    panel_a_path = os.path.join(
        config.OUTPUT_TABLE_DIR,
        "TableS9_PanelA_temporal_completeness.csv"
    )

    handle = open(panel_a_path, "wb")
    writer = csv.writer(handle)

    writer.writerow([
        "UA",
        "Coverage_ge5_pct",
        "Sink_ge5_MtCO2_yr",
        "Ratio_ge5",
        "Coverage_ge10_pct",
        "Sink_ge10_MtCO2_yr",
        "Ratio_ge10",
        "Coverage_ge15_pct",
        "Sink_ge15_MtCO2_yr",
        "Ratio_ge15"
    ])

    for ua in config.UA_ORDER:

        writer.writerow([
            ua,
            coverage[(ua, 5)],
            temporal[(ua, 5)]["sink"],
            temporal[(ua, 5)]["ratio"],
            coverage[(ua, 10)],
            temporal[(ua, 10)]["sink"],
            temporal[(ua, 10)]["ratio"],
            coverage[(ua, 15)],
            temporal[(ua, 15)]["sink"],
            temporal[(ua, 15)]["ratio"]
        ])

    handle.close()

    # Supporting Information Table S9 Panel B.
    panel_b_path = os.path.join(
        config.OUTPUT_TABLE_DIR,
        "TableS9_PanelB_benchmark_sensitivity.csv"
    )

    handle = open(panel_b_path, "wb")
    writer = csv.writer(handle)

    writer.writerow([
        "UA",
        "2060_remaining_industrial_emissions_MtCO2_yr",
        "Historical_sink_benchmark_MtCO2_yr",
        "Pressure_ratio_at_80pct",
        "Pressure_ratio_at_100pct",
        "Pressure_ratio_at_120pct"
    ])

    for ua in config.UA_ORDER:

        writer.writerow([
            ua,
            emissions[ua],
            sink[ua],
            benchmark[(ua, 80)]["ratio"],
            benchmark[(ua, 100)]["ratio"],
            benchmark[(ua, 120)]["ratio"]
        ])

    handle.close()

    # Fig. 7 data.
    fig7_main_path = os.path.join(
        config.OUTPUT_FIGURE_DATA_DIR,
        "Fig7_regional_totals_and_pressure_ratios.csv"
    )

    handle = open(fig7_main_path, "wb")
    writer = csv.writer(handle)

    writer.writerow([
        "UA",
        "Reported_Remaining_Emissions_MtCO2_yr",
        "Historical_Sink_Benchmark_MtCO2_yr",
        "Pressure_Ratio_80pct",
        "Pressure_Ratio_100pct",
        "Pressure_Ratio_120pct"
    ])

    for ua in config.UA_ORDER:

        writer.writerow([
            ua,
            emissions[ua],
            sink[ua],
            benchmark[(ua, 80)]["ratio"],
            benchmark[(ua, 100)]["ratio"],
            benchmark[(ua, 120)]["ratio"]
        ])

    handle.close()

    fig7_sector_path = os.path.join(
        config.OUTPUT_FIGURE_DATA_DIR,
        "Fig7_sector_remaining_emissions.csv"
    )

    handle = open(fig7_sector_path, "wb")
    writer = csv.writer(handle)

    writer.writerow([
        "UA",
        "Subsector",
        "Remaining_Emissions_MtCO2_yr"
    ])

    for row in sector_rows:
        writer.writerow([
            row["UA"],
            row["Subsector"],
            row["Remaining_Emissions_MtCO2_yr"]
        ])

    handle.close()

    # Fig. S1 data.
    figs1_path = os.path.join(
        config.OUTPUT_FIGURE_DATA_DIR,
        "FigS1_temporal_completeness_sensitivity.csv"
    )

    handle = open(figs1_path, "wb")
    writer = csv.writer(handle)

    writer.writerow([
        "UA",
        "Minimum_Valid_Years",
        "Coverage_pct",
        "Terrestrial_Sink_MtCO2_yr",
        "Pressure_Ratio"
    ])

    for ua in config.UA_ORDER:

        for threshold in config.TEMPORAL_THRESHOLDS:

            writer.writerow([
                ua,
                threshold,
                coverage[(ua, threshold)],
                temporal[(ua, threshold)]["sink"],
                temporal[(ua, threshold)]["ratio"]
            ])

    handle.close()

    print("  Manuscript outputs completed.")
    print("  Table 1: {0}".format(table1_path))
    print("  Table S9 Panel A: {0}".format(panel_a_path))
    print("  Table S9 Panel B: {0}".format(panel_b_path))


if __name__ == "__main__":

    try:
        run()
    except Exception:
        print(traceback.format_exc())
        raise
