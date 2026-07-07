陆地生态系统碳汇基准与工业排放压力评估

版本：1.0.0

## 一、代码包的复现范围

本代码包针对论文中“陆地生态系统碳汇基准与工业排放压力评估”部分。

代码对应以下论文内容：

- 正文方法第2.4节；
- 正文结果第3.5节；
- 正文Table 1；
- 正文Fig. 7；
- Supporting Information Method S5；
- Supporting Information Note S2；
- Supporting Information Table S9的Panel A和Panel B；
- Supporting Information Fig. S1。

## 二、代码包包含的分析

1. 检查年度NEP栅格、参考栅格、城市群边界和工业剩余排放输入；
2. 将年度NEP栅格投影并对齐至500 m等面积分析网格；
3. 统计每个像元在2001—2020年中的有效观测年份数；
4. 保留负NEP像元并计算像元长期平均NEP；
5. 计算至少5年、10年和15年有效观测阈值下的陆地碳汇基准；
6. 计算时间完整性阈值对覆盖率、碳汇基准和压力比的影响；
7. 计算历史碳汇基准为80%、100%和120%时的压力比敏感性；
8. 自动生成正文Table 1和补充材料Table S9两个Panel的数据；
9. 输出正文Fig. 7和补充材料Fig. S1所需的数据；
10. 提供最终Fig. 7和Fig. S1的MATLAB绘图代码；
11. 自动记录ArcGIS、Python和NumPy环境；
12. 将运行结果与已经核验的预期结果进行自动比对。

## 三、软件环境

原始工作流使用：

- ArcGIS Desktop 10.8；
- Python 2.7；
- ArcPy；
- Spatial Analyst；
- NumPy；
- MATLAB，绘制Fig. 7和Fig. S1。

ArcPy和Spatial Analyst需要ArcGIS许可。

## 四、数据目录

默认项目根目录为：

```text
C:\NEP
```

输入目录结构见：

```text
inputs\input_data_structure.txt
```

若实际项目路径不同，请修改`config.py`中的：

```python
PROJECT_ROOT = r"C:\NEP"
```

也可以通过Windows环境变量`NEP_PROJECT_ROOT`指定项目路径。

## 五、运行方法

使用ArcGIS Desktop 10.8自带的Python 2.7运行：

```text
C:\Python27\ArcGIS10.8\python.exe run_all.py
```

也可以双击：

```text
run_all.bat
```

代码依次执行：

```text
1. 输入检查
2. 年度NEP投影和网格对齐
3. 长期陆地碳汇基准计算
4. 两类压力比敏感性分析
5. 正文和补充材料表格、制图数据输出
6. 软件环境记录
7. 预期结果自动核验
```

## 六、关键输出

输出目录：

```text
C:\NEP\Reproducible_Outputs
```

### tables

- `main_results_ge10.csv`
- `sensitivity_ge5_ge10_ge15.csv`
- `pressure_ratio_temporal_thresholds.csv`
- `sink_capacity_sensitivity_80_100_120.csv`
- `source_sink_coupling_summary.csv`
- `sector_remaining_emissions_summary.csv`
- `Table1_main_text.csv`
- `TableS9_PanelA_temporal_completeness.csv`
- `TableS9_PanelB_benchmark_sensitivity.csv`

### figure_data

- `Fig7_regional_totals_and_pressure_ratios.csv`
- `Fig7_sector_remaining_emissions.csv`
- `FigS1_temporal_completeness_sensitivity.csv`

### rasters

- `UA_valid_year_count_2001_2020.tif`
- `UA_NEP_longterm_mean_ge5.tif`
- `UA_NEP_longterm_mean_ge10.tif`
- `UA_NEP_longterm_mean_ge15.tif`

### reports

- `input_validation_report.txt`
- `environment_details.txt`
- `expected_result_validation.txt`

## 七、已经核验的正文主结果

至少10年有效观测条件下，应得到：

| UA | Selected area (km²) | Coverage (%) | Mean NEP (g C m⁻² yr⁻¹) | Sink (Mt CO₂ yr⁻¹) |
|---|---:|---:|---:|---:|
| BTH | 196930.50 | 99.4193 | 177.2926 | 128.0192 |
| YRD | 186521.25 | 96.1906 | 217.5214 | 148.7653 |
| PRD | 33935.75 | 74.6320 | 261.9502 | 32.5947 |
| CP | 266604.75 | 98.7928 | 215.5248 | 210.6865 |

`tests\validate_expected_results.py`会自动检查这些值以及至少5年、10年和15年敏感性结果。

## 八、指标解释

工业排放压力比为：

```text
2060年DMS下工业剩余排放
/
2001—2020年长期陆地生态系统碳汇基准
```

该比值只用于比较工业剩余排放与区域整体陆地碳汇基准的相对量级。


80%、100%和120%条件是敏感性设置。

## 九、数据公开边界

本代码包不包含原始NEP栅格。使用者应从论文所述原始数据提供方获取年度NEP产品，并按输入结构配置文件。

仓库可公开：

- 分析代码；
- 参数设置；
- 输入文件规范；
- 汇总结果；
- 预期结果；
- 图表代码；
- 环境记录和复现说明。

## 十、论文中的Code Availability建议

> Code availability. The scripts used for NEP raster preprocessing, temporal completeness assessment, long-term terrestrial ecosystem sink benchmark construction, sensitivity analysis, and industrial emission pressure calculations are archived at [repository DOI]. The repository includes configuration files, input-data specifications, expected outputs, and the scripts used to generate the corresponding tables and figures. The original NEP raster data are not redistributed and should be obtained from the data provider identified in the manuscript.
