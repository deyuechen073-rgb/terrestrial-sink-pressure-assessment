# Mapping between manuscript elements and repository files

| Manuscript or SI element | Reproduced by |
|---|---|
| Main text Section 2.4, annual raster alignment | `scripts/project_nep_rasters.py` |
| Main text Eq. (10), long-term sink benchmark | `scripts/calculate_terrestrial_sink.py` |
| Main text Eq. (11), baseline pressure ratio | `scripts/calculate_pressure_ratios.py` |
| Main text Eqs. (12)-(13), 80%-120% benchmark sensitivity | `scripts/calculate_pressure_ratios.py` |
| Main text Table 1 | `scripts/build_manuscript_outputs.py` |
| Main text Fig. 7 | `matlab/Fig7_emission_sink_pressure_final.m` |
| SI Method S5, Eqs. (S5.1)-(S5.5) | `scripts/calculate_terrestrial_sink.py` |
| SI Method S5, Eq. (S5.6) | `scripts/calculate_pressure_ratios.py` |
| SI Note S2 and Table S9 Panel A | `scripts/build_manuscript_outputs.py` |
| SI Table S9 Panel B | `scripts/build_manuscript_outputs.py` |
| SI Fig. S1 | `matlab/FigS1_temporal_completeness_sensitivity.m` |
| Software environment record | `scripts/capture_environment.py` |
| Reproduction test | `tests/validate_expected_results.py` |

The package focuses on the terrestrial sink and industrial-pressure component.
Other analyses in the manuscript require separate datasets and code.
