# 비모수 데이터 통계 분석 가이드 (Codex-5.3)

## 1. 문서 목적과 사용 범위

이 문서는 비모수(nonparametric) 통계 분석을 프로젝트에서 재현 가능하게 수행하기 위한 기준 문서다.

1. 분석 방법 선택 기준을 통일한다.
2. 코드 구현 시 필요한 입력 조건과 통계 가정을 명시한다.
3. 결과 해석 문장과 보고서 구조를 표준화한다.
4. 실험 재현(코드, 노트북, 산출물 저장)을 보장한다.

문서의 1차 독자는 분석 코드 작성자이고, 2차 독자는 결과 보고서를 검토하는 실무 의사결정자다.

## 2. 비모수 통계 이론 핵심

### 2.1 비모수 vs 모수 통계

| 항목 | 모수 통계 | 비모수 통계 |
|---|---|---|
| 분포 가정 | 정규분포 등 명시적 가정 | 약한 가정 또는 분포 무가정 |
| 대표 통계량 | 평균, 분산 | 순위(rank), 중앙값, 부호 |
| 이상치 민감도 | 상대적으로 큼 | 상대적으로 낮음 |
| 검정력(power) | 가정 충족 시 높음 | 가정 위반 상황에서 안정적 |

핵심은 "비모수 = 소표본 전용"이 아니라 "분포 가정이 어렵거나 강건성이 중요할 때" 선택하는 방법이라는 점이다.

### 2.2 순위 기반 검정의 직관

많은 비모수 검정은 원자료 값을 순위로 변환해 통계량을 계산한다.  
그래서 극단값의 영향이 줄고, 단조 관계(monotonic relationship)를 안정적으로 포착한다.

### 2.3 공통 가정

방법별 세부 가정은 다르지만, 실무에서 다음은 기본으로 확인한다.

1. 관측치 독립성(또는 반복측정 구조의 명시)
2. 표본 추출 과정의 일관성
3. 결측치 처리 규칙의 사전 정의
4. 시간 데이터인 경우 자기상관(autocorrelation) 점검

### 2.4 장점과 한계

장점:
1. 분포 가정 위반 상황에서 강건
2. 이상치 영향 완화
3. 순서척도 데이터에 적합

한계:
1. 가정이 만족되는 모수 검정보다 검정력이 낮을 수 있음
2. 효과크기 해석이 직관적이지 않을 수 있음
3. 표본 설계가 나쁘면 비모수도 신뢰하기 어려움

### 2.5 p-value, 효과크기, 신뢰구간

보고 시 p-value 단독 해석은 금지한다. 최소 3가지를 함께 제시한다.

1. 유의성: p-value
2. 효과크기: rho, tau, Cliff's delta, rank-biserial 등
3. 불확실성: 신뢰구간 또는 부트스트랩 구간

## 3. 비모수 분석 적용 기준

다음 중 하나 이상이면 비모수 방법을 우선 검토한다.

1. 표본 수가 작아 정규성 판단이 불안정
2. 이상치가 많고 평균 기반 분석이 왜곡됨
3. 변수 척도가 순서형(ordinal)
4. 변수 관계가 선형보다 단조 관계에 가까움
5. 데이터 생성 메커니즘상 분포를 특정하기 어려움

## 4. 입력 데이터 스키마와 전처리 표준

분석 자동화를 위해 long/tidy 형태를 권장한다.

| 컬럼명 | 설명 | 예시 |
|---|---|---|
| `entity_id` | 개체 식별자 | `A001` |
| `time_index` | 시간/순서 인덱스 | `2025-01-01`, `1,2,3...` |
| `group` | 비교 그룹(선택) | `control`, `treatment` |
| `feature_*` | 분석 변수 | `feature_temp`, `feature_sales` |

전처리 표준:
1. 결측 처리 정책(삭제/대체/보간)을 feature별로 고정
2. 범위 규칙(min/max)과 단위 스케일 확인
3. 중복 키(`entity_id`, `time_index`) 검사
4. 분석 제외 레코드 사유를 로그로 보관

## 5. 분석 질문별 의사결정 표

| 분석 질문 | 데이터 구조 | 권장 방법 | 효과크기 | 후속 |
|---|---|---|---|---|
| 단일 feature에 단조 추세가 있는가 | 1변수 시계열/순서 | Mann-Kendall + Sen's slope | Sen's slope | 추세 방향 해석 |
| 단일 feature에 변곡점이 있는가 | 1변수 시계열/순서 | Pettitt test | 변화 전후 중앙값 차이 | 시점 이벤트 대조 |
| 독립 2그룹 분포가 다른가 | 2그룹 독립 표본 | Mann-Whitney U | rank-biserial, Cliff's delta | 그룹 정책 비교 |
| 대응 2조건 분포가 다른가 | paired 표본 | Wilcoxon signed-rank | matched rank-biserial | 전후 비교 |
| 독립 3그룹 이상 차이가 있는가 | 다집단 독립 표본 | Kruskal-Wallis | epsilon-squared | 사후검정(Dunn) |
| 반복측정 3조건 이상 차이가 있는가 | repeated measures | Friedman | Kendall's W | 사후검정(Wilcoxon+Holm) |
| feature 간 단조 상관이 있는가 | 연속/순서형 다변수 | Spearman rho, Kendall tau-b | rho, tau | FDR 보정 |
| 비선형 의존성이 있는가 | 다변수 | Distance correlation + permutation | dCor | permutation 기반 검증 |

## 6. 방법론 카드 (해석/보고서용)

### 6.1 Mann-Kendall + Sen's slope

- 목적: 단일 변수 추세 검정
- H0: 시간에 따른 단조 추세가 없다
- H1: 단조 증가 또는 감소 추세가 있다
- 출력: `tau`, `p-value`, `Sen's slope`
- 보고 예문: "`feature_x`는 시간에 따라 유의한 증가 추세를 보였다(tau=0.41, p=0.012, Sen's slope=0.83)."
- 주의: 자기상관이 강하면 p-value가 과소추정될 수 있다

### 6.2 Pettitt test

- 목적: 단일 변곡점(change point) 탐지
- H0: 시계열 분포에 변화점이 없다
- H1: 한 시점에서 분포가 변한다
- 출력: 변화 시점 인덱스, 통계량, p-value
- 보고 예문: "변화점은 t=38에서 탐지되었고(p=0.018), 이후 중앙값이 상승했다."
- 주의: 다중 변화점 데이터는 추가 알고리즘 병행 필요

### 6.3 Mann-Whitney U (독립 2그룹)

- 목적: 두 독립 그룹 분포 비교
- H0: 두 그룹 분포가 동일하다
- H1: 분포가 다르다
- 출력: U 통계량, p-value, 효과크기
- 주의: 위치 차이만이 아니라 분포 모양 차이에도 반응한다

### 6.4 Wilcoxon signed-rank (대응 2조건)

- 목적: 동일 대상의 전후/쌍 비교
- H0: 중앙 차이가 0이다
- H1: 중앙 차이가 0이 아니다
- 출력: W 통계량, p-value, 효과크기
- 주의: 차이값 분포가 대칭에 가까운지 확인

### 6.5 Kruskal-Wallis (독립 3그룹 이상)

- 목적: 다집단 분포 차이 검정
- H0: 모든 그룹 분포가 동일하다
- H1: 적어도 한 그룹이 다르다
- 출력: H 통계량, p-value
- 후속: 사후검정(Dunn test) + 다중비교 보정

### 6.6 Friedman (반복측정 3조건 이상)

- 목적: 반복측정 조건 간 차이 검정
- H0: 조건 간 차이가 없다
- H1: 조건 간 차이가 있다
- 출력: chi-square 통계량, p-value, Kendall's W
- 후속: 대응 Wilcoxon 사후검정 + Holm/FDR 보정

### 6.7 Spearman rho / Kendall tau-b

- 목적: feature 간 단조 상관 추정
- H0: 순위 상관이 0이다
- H1: 순위 상관이 0이 아니다
- 출력: 상관계수, p-value, 보정 p-value
- 주의: 상관은 인과를 의미하지 않는다

### 6.8 Distance correlation + permutation

- 목적: 비선형 의존성 검정
- H0: 두 변수는 독립이다
- H1: 독립이 아니다
- 출력: dCor, permutation p-value
- 주의: 계산량이 커서 permutation 횟수와 시간 예산을 함께 관리

## 7. 다중검정 보정 규칙

다수 feature를 동시에 비교하면 거짓양성(False Discovery)이 증가한다.  
기본 규칙은 Benjamini-Hochberg(FDR) 보정을 사용한다.

1. 동일 분석군에서 계산된 p-value를 하나의 family로 묶는다.
2. 원 p-value와 보정 p-value를 함께 저장한다.
3. 보고서에는 "보정 후 유의 여부"를 기준으로 결론을 작성한다.

## 8. 결과 해석 표준과 문장 템플릿

### 8.1 해석 표준

1. 통계적 유의성(p-value)과 실질적 중요도(효과크기)를 분리해 기술
2. 표본 수와 결측률을 결과 표 상단에 명시
3. 검정 가정 위반 가능성을 한계 섹션에 기록
4. 다중검정 수행 시 보정 방법을 본문에서 명시

### 8.2 문장 템플릿

추세 분석:
"`feature_x`는 기간 `[t0, t1]`에서 유의한 [증가/감소] 추세를 보였다(tau=`{tau}`, p=`{p}`, slope=`{slope}`)."

변곡점 분석:
"Pettitt 검정 결과 변화점은 `{cp_index}`로 탐지되었고(p=`{p}`), 전후 중앙값은 `{med_before}`에서 `{med_after}`로 변했다."

상관 분석:
"`feature_a`와 `feature_b`의 Spearman 상관은 `{rho}`였고, FDR 보정 후 p-value는 `{p_adj}`였다."

정합성 검증:
"총 `{n_total}`건 중 규칙 위반은 `{n_bad}`건(`{ratio}%`)으로 확인되었으며, 주요 위반 유형은 `{rule_name}`이었다."

## 9. 보고서 작성 템플릿

아래 목차를 고정 포맷으로 사용한다.

1. 분석 목적과 의사결정 질문
2. 데이터 설명(기간, 표본 수, 결측/제외 기준)
3. 분석 방법 선택 근거(왜 해당 비모수 검정을 썼는지)
4. 주요 결과(표 + 그림 + 핵심 수치)
5. 통계 해석(유의성, 효과크기, 불확실성)
6. 비즈니스 해석(업무 영향, 우선순위)
7. 한계와 리스크(가정 위반 가능성, 표본 편향)
8. 후속 액션(추가 데이터 수집, 실험 계획, 모니터링 지표)
9. 재현 정보(코드 경로, 실행 명령, 패키지 버전, seed)

## 10. 구현 가이드 (코드/노트북)

### 10.1 권장 파일 구조

```text
.
├── src/nonparametric_analysis/
│   └── analysis/
│       ├── nonparametric_methods.py
│       └── integrity_checks.py
├── scripts/
│   └── run_nonparametric_analysis.py
└── notebooks/
    └── nonparametric_analysis_template.ipynb
```

### 10.2 권장 의존성 설치

```bash
uv add numpy pandas scipy matplotlib seaborn jupyter
uv add --dev pytest
```

### 10.3 실행 스크립트 최소 규격

`scripts/run_nonparametric_analysis.py`는 다음을 반드시 수행한다.

1. 입력 데이터 로드
2. 정합성 검사(결측/범위/중복)
3. 비모수 검정 실행
4. 결과 저장(`summary.csv`, `*_corr.csv`)
5. 시각화 저장(`change_point.png`, `spearman_heatmap.png`)

### 10.4 노트북 최소 셀 구조

1. 분석 목적/가설(Markdown)
2. 라이브러리 import(Code)
3. 데이터 로드/전처리(Code)
4. 정합성 리포트(Code + Markdown)
5. 추세/변곡점 분석(Code + Plot)
6. 상관성/다중검정 보정(Code + Heatmap)
7. 결론/한계/후속조치(Markdown)

### 10.5 샘플 데이터 기반 실행/검증 예시

아래는 저장소에 포함된 실제 스크립트 기준 실행 예시다.

```bash
# 1) 샘플 데이터 생성
python3 scripts/generate_sample_dataset.py \
  --output data/sample_nonparametric.csv \
  --n-rows 120 \
  --seed 42

# 2) 비모수 분석 실행
python3 scripts/run_nonparametric_analysis.py \
  --input data/sample_nonparametric.csv \
  --output outputs/nonparametric_run \
  --alpha 0.05
```

정상 실행 시 주요 결과 파일:
1. `outputs/nonparametric_run/summary.csv`
2. `outputs/nonparametric_run/integrity_summary.csv`
3. `outputs/nonparametric_run/spearman_corr.csv`
4. `outputs/nonparametric_run/change_point.png`
5. `outputs/nonparametric_run/analysis_report.md`

검증 포인트:
1. `summary.csv`에서 `pettitt_p_value`, `mann_kendall_p_value`가 유의 수준 이하인지 확인
2. `integrity_summary.csv`에서 결측/중복/규칙 위반 개수 확인
3. `analysis_report.md`의 해석 문장이 통계 결과와 일치하는지 확인

## 11. 실행 체크리스트

분석 실행 전:
1. 데이터 스키마 확정(`entity_id`, `time_index`, `feature_*`)
2. 결측 처리 정책 확정
3. 유의수준(alpha) 및 보정 전략 확정
4. 재현 seed와 패키지 버전 고정

분석 실행 후:
1. 결과 파일(csv/png/ipynb) 아카이빙
2. 보고서에 "통계 해석 + 업무 해석" 동시 기재
3. 사용한 코드 경로와 실행 명령 기록

## 12. 오해 방지 메모

1. "비모수라서 아무 가정도 없다"는 잘못된 표현이다.
2. "p<0.05면 중요하다"는 결론은 효과크기 없이 불완전하다.
3. "상관이 있다 = 인과가 있다"는 해석은 금지한다.
4. "변곡점 탐지 결과 1개"를 절대적 사실로 단정하지 않는다.

---

필요하면 다음 단계로 이 문서 기준의 실제 코드 파일(`nonparametric_methods.py`, `run_nonparametric_analysis.py`)과 노트북 템플릿(`notebooks/nonparametric_analysis_template.ipynb`)을 저장소에 바로 생성한다.
