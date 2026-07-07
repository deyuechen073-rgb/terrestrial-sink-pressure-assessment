# Repository release checklist

Before creating the public release:

- [ ] Remove personal local paths from `config.py`.
- [ ] Confirm that no restricted raw data are included.
- [ ] Run `run_all.py` from a clean output directory.
- [ ] Confirm that `expected_result_validation.txt` reports `PASSED`.
- [ ] Check all four valid-year-count rasters in ArcGIS.
- [ ] Run the final Fig. 7 MATLAB script.
- [ ] Run the Fig. S1 MATLAB script.
- [ ] Confirm that Table 1 and Table S9 values match the manuscript.
- [ ] Record the exact ArcGIS, Python, NumPy, and MATLAB versions.
- [ ] Create a GitHub release tagged `v1.0.0`.
- [ ] Archive the release in Zenodo and obtain a DOI.
- [ ] Replace `[repository DOI]` in the manuscript statements.
- [ ] Cite the fixed release rather than a changing branch.
