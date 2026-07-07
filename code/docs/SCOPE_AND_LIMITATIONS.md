# Scope and limitations

1. The code reproduces the terrestrial ecosystem sink benchmark and industrial
   emission pressure assessment only.

2. The 2001-2020 mean NEP is an observational historical benchmark. It is not
   presented as a deterministic estimate of ecosystem carbon uptake in 2060.

3. The 80%, 100%, and 120% conditions are sensitivity settings.

4. The industrial emission pressure ratio uses regional terrestrial ecosystem
   carbon uptake as a regional benchmark. It does not allocate ecosystem sinks
   to industry.

5. The original workflow requires ArcGIS Desktop 10.8, ArcPy, and a Spatial
   Analyst licence. This reduces portability but preserves the environment in
   which the reported results were generated.

6. Original annual NEP rasters are not included in this repository. Users must
   obtain them from the source identified in the manuscript.

7. The expected-result test checks numerical reproducibility for the validated
   input rasters and boundary files. Different versions of the source data,
   administrative boundaries, reprojection algorithms, or raster alignment
   settings may produce different results.
