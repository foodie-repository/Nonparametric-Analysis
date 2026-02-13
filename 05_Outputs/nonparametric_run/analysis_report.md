# Nonparametric Analysis Report

## 1. Run Configuration
- Input data: `data/sample_nonparametric.csv`
- Output directory: `outputs/nonparametric_run`
- Alpha: `0.05`

## 2. Trend & Change-Point
- Pettitt change index: `61`
- Pettitt change time: `62.00`
- Pettitt p-value: `0.000000`
- Mann-Kendall tau: `0.8693`
- Mann-Kendall p-value: `0.000000`
- Sen's slope: `0.3316`

## 3. Integrity Check Summary
- Row count: `120`
- Duplicate rows (`entity_id`,`time_index`): `2`
- Range violations (feature_1): `4`
- MAD outliers (feature_1): `1`
- Formula violations (feature_total): `8`

## 4. Output Files
- `summary.csv`, `integrity_summary.csv`
- `spearman_corr.csv`, `spearman_p_value.csv`, `spearman_p_value_fdr.csv`
- `kendall_corr.csv`, `kendall_p_value.csv`, `kendall_p_value_fdr.csv`
- `missing_report.csv`, `duplicate_rows.csv`
- `range_violations_feature_1.csv`, `mad_outliers_feature_1.csv`, `formula_violations.csv`
- `change_point.png`, `spearman_heatmap.png`, `feature_boxplot.png`
