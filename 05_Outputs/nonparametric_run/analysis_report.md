# 비모수 분석 결과 보고서

## 1. 실행 설정
- 입력 데이터: `data/sample_nonparametric.csv`
- 출력 디렉토리: `outputs/nonparametric_run`
- 유의수준 (α): `0.05`

## 2. 추세 및 변곡점 분석
- Pettitt 변곡점 위치: `61`
- Pettitt 변곡점 시점: `62.00`
- Pettitt p-값: `0.000000` ✅ (유의미한 변곡점)
- Mann-Kendall 타우: `0.8693`
- Mann-Kendall p-값: `0.000000` ✅ (유의미한 상승 추세)
- Sen's 기울기: `0.3316` (시간당 증가율)

## 3. 데이터 정합성 검사 요약
- 총 행 수: `120`
- 중복 행 (`entity_id`, `time_index`): `2` ⚠️
- 범위 위반 (feature_1): `4` ⚠️
- MAD 이상치 (feature_1): `1` ⚠️
- 수식 위반 (feature_total): `8` ⚠️

## 4. 생성된 결과 파일

### CSV 파일
- `summary.csv` - 전체 분석 요약
- `integrity_summary.csv` - 정합성 검사 요약
- `spearman_corr.csv` - Spearman 상관계수 행렬
- `spearman_p_value.csv` - Spearman p-값 행렬
- `spearman_p_value_fdr.csv` - FDR 보정된 p-값
- `kendall_corr.csv` - Kendall 상관계수 행렬
- `kendall_p_value.csv` - Kendall p-값 행렬
- `kendall_p_value_fdr.csv` - FDR 보정된 p-값
- `missing_report.csv` - 결측치 상세 리포트
- `duplicate_rows.csv` - 중복 행 리스트
- `range_violations_feature_1.csv` - 범위 위반 상세
- `mad_outliers_feature_1.csv` - 이상치 상세
- `formula_violations.csv` - 수식 위반 상세

### 시각화 파일
- `change_point.png` - 변곡점 시각화
- `spearman_heatmap.png` - Spearman 상관 히트맵
- `feature_boxplot.png` - 변수별 박스플롯
