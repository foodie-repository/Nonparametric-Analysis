# 비모수 데이터 통계 분석 Spec

> **목적:** AI 에이전트가 비모수 분석 코드를 작성·실행·시각화할 때 참조하는 사양서  
> **참조:** 이론적 배경은 `02_비모수_분석_이론가이드.md`, 보고서 형식은 `03_비모수_보고서_템플릿.md` 참조

---

## 1. 입력 데이터 스키마

분석 대상 데이터는 long/tidy 형태를 기본으로 한다.

| 컬럼명 | 타입 | 필수 | 설명 | 예시 |
|--------|------|------|------|------|
| `entity_id` | str | ✅ | 개체 식별자 | `A001` |
| `time_index` | int/date | ○ | 시간/순서 인덱스 | `2025-01-01`, `1,2,3…` |
| `group` | str | ○ | 비교 그룹 (2그룹 이상일 때) | `control`, `treatment` |
| `feature_*` | float/int | ✅ | 분석 변수 (1개 이상) | `feature_temp`, `feature_sales` |

### 전처리 표준

1. **결측 처리:** feature별로 정책 고정 (삭제/중앙값 대체/보간). 처리 내역을 로그로 보관
2. **범위 검사:** min/max 허용 범위를 사전 정의. 범위 초과 시 이상치 플래그
3. **중복 검사:** `(entity_id, time_index)` 키 기준 중복 제거
4. **제외 레코드:** 사유를 `exclusion_log.csv`에 기록

---

## 2. 분석 방법 선택 의사결정 표

### 2.1 정규성 판단 (전제 단계)

| 조건 | 판단 | 후속 |
|------|------|------|
| Shapiro-Wilk p ≥ 0.05 **및** Q-Q 플롯 정상 | 정규 가정 가능 | 모수 검정 고려 |
| p < 0.05 **또는** n < 30 **또는** 순서형 데이터 | 비모수 검정 적용 | 아래 표 참조 |

### 2.2 분석 질문 → 검정 방법 매핑

| # | 분석 질문 | 데이터 구조 | 검정 방법 | 효과 크기 | 사후 검정 |
|---|----------|------------|----------|----------|----------|
| 1 | 단일 feature에 단조 추세가 있는가 | 1변수 시계열 | Mann-Kendall | Sen's slope, τ | — |
| 2 | 단일 feature에 변곡점이 있는가 | 1변수 시계열 | Pettitt test / PELT | 전후 중앙값 차이 | 구간별 Mann-Whitney |
| 3 | 중앙값이 특정 값과 같은가 | 1변수 | Wilcoxon 부호순위 | r = \|Z\|/√N | — |
| 4 | 독립 2그룹 분포가 다른가 | 2그룹 독립 | Mann-Whitney U | r, CLES, Cliff's δ | — |
| 5 | 대응 2조건 분포가 다른가 | paired 표본 | Wilcoxon signed-rank | r, matched rank-biserial | — |
| 6 | 2그룹 분포 형태가 다른가 | 2그룹 독립 | Kolmogorov-Smirnov | D 통계량 | — |
| 7 | 독립 3그룹+ 차이가 있는가 | 다집단 독립 | Kruskal-Wallis | η² (epsilon-squared) | Dunn + Bonferroni |
| 8 | 반복측정 3조건+ 차이가 있는가 | repeated measures | Friedman | Kendall's W | Wilcoxon 쌍별 + Holm |
| 9 | feature 간 단조 상관이 있는가 | 다변수 | Spearman ρ / Kendall τ | ρ, τ | FDR 보정 |
| 10 | 비선형 의존성이 있는가 | 다변수 | Distance Correlation | dCor | Permutation 검정 |
| 11 | 추정값의 신뢰구간은? | 모든 데이터 | Bootstrap | SE, CI | — |
| 12 | 그룹 차이가 우연인가? | 2그룹 | Permutation Test | 관측 차이 | — |
| 13 | 데이터에 패턴이 있는가? | 시계열 | Runs Test | Z | — |

---

## 3. 검정별 입출력 규격

### 3.1 Mann-Kendall + Sen's slope

```
입력: feature 배열 (시간순 정렬), alpha
출력: {tau, p_value, sens_slope, trend_direction}
시각화: 시계열 + Sen's slope 직선 + 추세 방향 표시
```

### 3.2 Pettitt test

```
입력: feature 배열 (시간순 정렬), alpha
출력: {change_point_index, statistic, p_value, median_before, median_after}
시각화: 시계열 + 변곡점 수직선 + 전후 구간 중앙값 수평선
```

### 3.3 PELT (다중 변곡점)

```
입력: feature 배열, model("rbf"), penalty(None=BIC 자동)
출력: {changepoints: [인덱스 리스트], n_segments}
시각화: 시계열 + 변곡점 수직선 + 구간별 중앙값 + 구간별 박스플롯
```

### 3.4 Shapiro-Wilk

```
입력: feature 배열, alpha
출력: {W, p_value, is_normal}
시각화: 히스토그램+KDE, Q-Q 플롯, 박스플롯 (3-panel)
```

### 3.5 Wilcoxon 부호순위 (단일 표본)

```
입력: feature 배열, hypothesized_median, alpha
출력: {T, Z, p_value, effect_size_r}
시각화: 박스플롯 + 가설 중앙값 vs 표본 중앙값 표시
```

### 3.6 Mann-Whitney U

```
입력: group1 배열, group2 배열, alpha
출력: {U, Z, p_value, effect_size_r, cles, cliffs_delta}
시각화: 박스플롯+개별 포인트, 순위 분포 히스토그램 (2-panel)
```

### 3.7 Wilcoxon signed-rank (대응)

```
입력: before 배열, after 배열, alpha
출력: {T, Z, p_value, effect_size_r, median_diff}
시각화: Spaghetti plot (사전→사후), 차이값 히스토그램 (2-panel)
```

### 3.8 Kolmogorov-Smirnov

```
입력: group1 배열, group2 배열
출력: {D, p_value}
시각화: ECDF 비교 플롯
```

### 3.9 Kruskal-Wallis + Dunn

```
입력: *groups (3개 이상 배열), group_names, alpha
출력: {H, p_value, eta_squared, dunn_posthoc(DataFrame, 유의시)}
시각화: 박스플롯+포인트 오버레이, Dunn p-value 히트맵 (유의시)
```

### 3.10 Friedman

```
입력: *conditions (3개 이상 대응 배열), condition_names
출력: {chi2, p_value, kendall_w}
시각화: Spaghetti plot + 중앙값 라인, 조건별 박스플롯 (2-panel)
```

### 3.11 Spearman / Kendall

```
입력: x 배열, y 배열
출력: {rho/tau, p_value}
시각화: 원본 산점도, 순위 변환 산점도 (2-panel)
```

### 3.12 다변량 상관 매트릭스

```
입력: DataFrame (feature 컬럼들), method('spearman'/'kendall')
출력: {correlation_matrix, p_value_matrix}
시각화: 상관 히트맵 + p-value 히트맵 (2-panel, 하삼각)
```

### 3.13 Distance Correlation

```
입력: x 배열, y 배열, n_permutations
출력: {dcor, p_value}
시각화: 산점도 + permutation 분포 히스토그램
```

### 3.14 Bootstrap 신뢰구간

```
입력: data 배열, stat_func(np.median), n_boot(10000), ci(95)
출력: {observed, ci_lower, ci_upper, se}
시각화: Bootstrap 분포 히스토그램 + 관측값 + CI 영역
```

### 3.15 Permutation Test

```
입력: group1, group2, stat_func, n_perm(10000)
출력: {observed_diff, p_value}
시각화: 순열 분포 히스토그램 + 관측 차이 수직선
```

### 3.16 Runs Test

```
입력: data 배열 (시계열)
출력: {runs, expected_runs, Z, p_value}
시각화: 시계열+중앙값 면적 채우기, 이진 시퀀스 (2-panel)
```

---

## 4. 다중검정 보정 규칙

동일 분석군에서 복수 feature 또는 복수 쌍을 검정할 때 적용한다.

| 상황 | 보정 방법 | 적용 예 |
|------|----------|--------|
| 사후 검정 (Dunn) | Bonferroni | Kruskal-Wallis 이후 |
| 사후 검정 (Friedman) | Holm | Friedman 이후 Wilcoxon 쌍별 |
| 상관 매트릭스 | Benjamini-Hochberg (FDR) | 다변수 Spearman |
| 기타 다중 비교 | FDR 기본, 보수적 필요시 Bonferroni | — |

**규칙:**
1. 원 p-value와 보정 p-value를 모두 저장
2. 보고서에는 **보정 후** 유의 여부 기준으로 결론 작성
3. 보정 방법을 보고서에 명시

---

## 5. 산출물 파일 규격

### 5.1 디렉토리 구조

```
outputs/{run_name}/
├── summary.csv               # 모든 검정 결과 요약 (1행 = 1검정)
├── integrity_summary.csv      # 전처리 정합성 보고
├── correlation_matrix.csv     # 상관 매트릭스 (유의시)
├── figures/
│   ├── normality_{feature}.png
│   ├── mann_whitney_{g1}_vs_{g2}.png
│   ├── changepoint_{feature}.png
│   ├── spearman_heatmap.png
│   └── bootstrap_{stat}.png
└── analysis_report.md         # 최종 보고서 (03_템플릿 형식)
```

### 5.2 summary.csv 스키마

| 컬럼 | 설명 |
|------|------|
| `test_name` | 검정 이름 (`mann_whitney_u`, `kruskal_wallis` 등) |
| `feature` | 분석 대상 feature명 |
| `group1` / `group2` | 비교 그룹명 (해당시) |
| `statistic` | 검정 통계량 |
| `p_value` | 원 p-value |
| `p_value_adj` | 보정 p-value (해당시) |
| `effect_size` | 효과 크기 값 |
| `effect_size_type` | 효과 크기 종류 (`r`, `eta_sq`, `cles` 등) |
| `significant` | 유의 여부 (True/False) |
| `alpha` | 사용된 유의수준 |

---

## 6. 시각화 표준

### 6.1 공통 설정

```python
plt.rcParams['font.family'] = 'AppleGothic'  # macOS 한글
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style="whitegrid", font="AppleGothic")
```

### 6.2 차트 규칙

| 항목 | 규칙 |
|------|------|
| 파일 형식 | PNG (300 DPI) |
| 제목 | 검정명 + 주요 통계량 포함 |
| 유의수준 표시 | 빨간 점선으로 α=0.05 기준선 |
| 색상 | 그룹 비교: Set3 팔레트, 유의/비유의: 빨강/회색 |
| figsize | 단일 패널 (10,5), 2패널 (12,5), 3패널 (15,4) |

---

## 7. 효과 크기 판정 기준

| 지표 | 사용 검정 | 작은 | 중간 | 큰 |
|------|----------|------|------|-----|
| r (= \|Z\|/√N) | Mann-Whitney, Wilcoxon | 0.10 | 0.30 | 0.50 |
| CLES (P(X>Y)) | Mann-Whitney | 0.56 | 0.64 | 0.71 |
| Cliff's δ | Mann-Whitney | 0.15 | 0.33 | 0.47 |
| η² (epsilon²) | Kruskal-Wallis | 0.01 | 0.06 | 0.14 |
| Kendall's W | Friedman | 0.10 | 0.30 | 0.50 |
| ρ (Spearman) | 상관분석 | 0.10 | 0.30 | 0.50 |
| τ (Kendall) | 상관분석 | 0.10 | 0.20 | 0.30 |

---

## 8. 실행 체크리스트

### 실행 전
- [ ] 데이터 스키마 확정 (`entity_id`, `time_index`, `feature_*`)
- [ ] 결측 처리 정책 확정
- [ ] 유의수준(α) 및 다중검정 보정 전략 확정
- [ ] 재현 seed와 패키지 버전 고정

### 실행 후
- [ ] `summary.csv` 생성 및 유의 검정 확인
- [ ] `integrity_summary.csv` 의 결측/중복/위반 건수 확인
- [ ] 시각화 파일이 `figures/` 에 모두 저장되었는지 확인
- [ ] `analysis_report.md` 해석 문장이 통계 결과와 일치하는지 확인
- [ ] 사용한 코드 경로·실행 명령·패키지 버전 기록
