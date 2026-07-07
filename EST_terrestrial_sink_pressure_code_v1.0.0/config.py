# -*- coding: utf-8 -*-
"""
Configuration for the terrestrial ecosystem sink benchmark and
industrial emission pressure assessment.

Original execution environment:
- ArcGIS Desktop 10.8
- Python 2.7
- ArcPy
- Spatial Analyst
"""

import os

PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))

# The project root can be overridden through the Windows environment
# variable NEP_PROJECT_ROOT.
PROJECT_ROOT = os.environ.get("NEP_PROJECT_ROOT", r"C:\NEP")

ORIGINAL_NEP_DIR = os.path.join(PROJECT_ROOT, "Original")
PROJECTED_NEP_DIR = os.path.join(PROJECT_ROOT, "Projected")
BOUNDARY_DIR = os.path.join(PROJECT_ROOT, "Boundary_Albers")

OUTPUT_ROOT = os.path.join(PROJECT_ROOT, "Reproducible_Outputs")
OUTPUT_RASTER_DIR = os.path.join(OUTPUT_ROOT, "rasters")
OUTPUT_TABLE_DIR = os.path.join(OUTPUT_ROOT, "tables")
OUTPUT_FIGURE_DATA_DIR = os.path.join(OUTPUT_ROOT, "figure_data")
OUTPUT_REPORT_DIR = os.path.join(OUTPUT_ROOT, "reports")
TEMP_DIR = os.path.join(OUTPUT_ROOT, "temp")

REFERENCE_RASTER = os.path.join(
    PROJECTED_NEP_DIR,
    "NEP_2001_Albers.tif"
)

YEAR_START = 2001
YEAR_END = 2020
YEARS = range(YEAR_START, YEAR_END + 1)

TARGET_CELL_SIZE_M = 500.0
RESAMPLING_METHOD = "BILINEAR"

MAIN_THRESHOLD = 10
TEMPORAL_THRESHOLDS = [5, 10, 15]
ALL_COVERAGE_THRESHOLDS = range(1, 21)

SINK_CAPACITY_SCALES = [0.8, 1.0, 1.2]

UA_ORDER = ["BTH", "YRD", "PRD", "CP"]

BOUNDARIES = {
    "BTH": os.path.join(
        BOUNDARY_DIR,
        "BTH_boundary_Albers.shp"
    ),
    "YRD": os.path.join(
        BOUNDARY_DIR,
        "YRD_boundary_Albers.shp"
    ),
    "PRD": os.path.join(
        BOUNDARY_DIR,
        "PRD_boundary_Albers.shp"
    ),
    "CP": os.path.join(
        BOUNDARY_DIR,
        "CP_boundary_Albers.shp"
    )
}

INDUSTRIAL_EMISSIONS_CSV = os.path.join(
    PACKAGE_ROOT,
    "inputs",
    "industrial_remaining_emissions_2060.csv"
)

SECTOR_REMAINING_EMISSIONS_CSV = os.path.join(
    PACKAGE_ROOT,
    "inputs",
    "sector_remaining_emissions_2060.csv"
)

EXPECTED_MAIN_RESULTS_CSV = os.path.join(
    PACKAGE_ROOT,
    "expected_outputs",
    "main_results_ge10_expected.csv"
)

EXPECTED_TEMPORAL_SENSITIVITY_CSV = os.path.join(
    PACKAGE_ROOT,
    "expected_outputs",
    "sensitivity_ge5_ge10_ge15_expected.csv"
)

# Existing projected rasters are preserved by default.
OVERWRITE_PROJECTED_RASTERS = False

# Analysis outputs are replaced when the pipeline is rerun.
OVERWRITE_ANALYSIS_OUTPUTS = True

RUN_PROJECTION_STEP = True
RUN_EXPECTED_RESULT_CHECK = True

# Broad limits used only to remove NoData sentinels and corrupted values.
VALID_NEP_MIN = -1.0e20
VALID_NEP_MAX = 1.0e20

# Reproducibility-test tolerances.
SINK_ABS_TOLERANCE_MTCO2_YR = 0.02
AREA_ABS_TOLERANCE_KM2 = 0.30
COVERAGE_ABS_TOLERANCE_PCT = 0.02
MEAN_NEP_ABS_TOLERANCE = 0.02
