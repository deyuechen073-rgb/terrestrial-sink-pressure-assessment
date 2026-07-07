# Terrestrial Ecosystem Sink Benchmark and Industrial Emission Pressure Assessment

Version 1.0.0

This repository reproduces the terrestrial ecosystem sink benchmark and
industrial emission pressure assessment reported in the manuscript.

## Scope

The package covers:

- Methods Section 2.4;
- Results Section 3.5;
- main-text Table 1 and Fig. 7;
- Supporting Information Method S5 and Note S2;
- Supporting Information Table S9 and Fig. S1.

It does not claim to reproduce the full city-subsector inventory, LMDI
decomposition, or MESSAGEix scenario model.

## Environment

- ArcGIS Desktop 10.8
- Python 2.7
- ArcPy
- Spatial Analyst
- NumPy
- MATLAB for Fig. 7 and Fig. S1

## Run

Edit `config.py` if the project root is not `C:\NEP`, then execute:

```text
C:\Python27\ArcGIS10.8\python.exe run_all.py
```

See `README_CN.md` for the complete workflow, interpretation rules, expected
results, and output descriptions.
