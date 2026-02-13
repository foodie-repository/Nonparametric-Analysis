# Nonparametric Analysis

비모수 통계 분석을 코드로 실행하고, 결과를 시각화/보고서 형태로 정리하기 위한 프로젝트입니다.

현재 저장소는 `분석 스펙(01)` → `데이터(02)` → `코드(03)` → `노트북(04)` → `결과물(05)` 흐름으로 구성되어 있습니다.

## 한눈에 보기

- 분석 사양/이론/보고서 템플릿 문서: `01_Specs/`
- 분석 패키지 운영 매뉴얼: `01_Specs/04_비모수_분석_패키지_가이드.md`
- 샘플 및 입력 데이터: `02_Data/`
- 핵심 분석 코드/실행 스크립트: `03_Code/`
- 탐색/시각화 노트북: `04_Notebooks/`
- 실행 결과 및 리포트: `05_Outputs/`
- 레거시/보관 문서: `99_Archive/`
- API 스켈레톤(FastAPI): `main.py`

## 프로젝트 구조

```text
.
├── 01_Specs/
│   ├── 01_비모수_분석_spec.md
│   ├── 02_비모수_분석_이론가이드.md
│   ├── 03_비모수_보고서_템플릿.md
│   └── 04_비모수_분석_패키지_가이드.md
├── 02_Data/
│   └── sample_nonparametric.csv
├── 03_Code/
│   ├── scripts/
│   │   ├── generate_sample_dataset.py
│   │   └── run_nonparametric_analysis.py
│   └── src/nonparametric_analysis/analysis/
│       ├── nonparametric_methods.py
│       ├── integrity_checks.py
│       ├── sample_data.py
│       ├── utils.py
│       └── visualizations.py
├── 04_Notebooks/
│   └── nonparametric_analysis_template.ipynb
├── 05_Outputs/
│   ├── nonparametric_run/
│   └── nonparametric_analysis_walkthrough.md
├── tests/
├── main.py
├── pyproject.toml
└── README.md
```

## 작업별 빠른 네비게이션

| 하고 싶은 작업 | 먼저 볼 폴더/문서 | 다음으로 볼 코드/결과 |
|---|---|---|
| 비모수 분석 기준 파악 | `01_Specs/01_비모수_분석_spec.md` | `03_Code/src/nonparametric_analysis/analysis/nonparametric_methods.py` |
| 이론/해석 근거 확인 | `01_Specs/02_비모수_분석_이론가이드.md` | `05_Outputs/nonparametric_run/summary.csv` |
| 보고서 작성 형식 확인 | `01_Specs/03_비모수_보고서_템플릿.md` | `05_Outputs/nonparametric_run/analysis_report.md` |
| 패키지 사용법/함수 개요 확인 | `01_Specs/04_비모수_분석_패키지_가이드.md` | `03_Code/src/nonparametric_analysis/analysis/` |
| 샘플 데이터 생성 | `03_Code/scripts/generate_sample_dataset.py` | `02_Data/sample_nonparametric.csv` |
| 전체 분석 실행 | `03_Code/scripts/run_nonparametric_analysis.py` | `05_Outputs/nonparametric_run/` |
| 정합성 규칙 수정 | `03_Code/src/nonparametric_analysis/analysis/integrity_checks.py` | `05_Outputs/nonparametric_run/integrity_check.csv` |
| 추세/변곡점 로직 수정 | `03_Code/src/nonparametric_analysis/analysis/nonparametric_methods.py` | `05_Outputs/nonparametric_run/figures/*pettitt*.png`, `*mk*.png` |
| 상관/FDR 로직 수정 | `03_Code/src/nonparametric_analysis/analysis/utils.py` | `05_Outputs/nonparametric_run/correlation_pvalues_adjusted.csv` |
| 노트북 기반 탐색 분석 | `04_Notebooks/nonparametric_analysis_template.ipynb` | `05_Outputs/notebook_demo/` |
| API 엔드포인트 작업 | `main.py` | `tests/test_main.py` |

## 빠른 시작

```bash
# 1) 의존성 설치
uv sync --extra dev
```

## 샘플 데이터 생성 + 분석 실행

```bash
# 2) 샘플 데이터 생성
uv run python 03_Code/scripts/generate_sample_dataset.py \
  --output 02_Data/sample_nonparametric.csv \
  --n-rows 120 \
  --seed 42

# 3) 비모수 분석 실행
uv run python 03_Code/scripts/run_nonparametric_analysis.py \
  --input 02_Data/sample_nonparametric.csv \
  --output 05_Outputs/nonparametric_run
```

실행 후 주요 산출물:

- `05_Outputs/nonparametric_run/summary.csv`
- `05_Outputs/nonparametric_run/integrity_check.csv`
- `05_Outputs/nonparametric_run/correlation_pvalues_adjusted.csv`
- `05_Outputs/nonparametric_run/figures/*.png`

## 노트북 실행

- 템플릿: `04_Notebooks/nonparametric_analysis_template.ipynb`
- 목적: 탐색 분석, 시각화 확인, 결과 해석 초안 작성

## 테스트

```bash
# API 기본 테스트
uv run python -m pytest tests/test_main.py
```

## 문서 읽기 순서 추천

1. `01_Specs/01_비모수_분석_spec.md`
2. `01_Specs/02_비모수_분석_이론가이드.md`
3. `01_Specs/03_비모수_보고서_템플릿.md`
4. `01_Specs/04_비모수_분석_패키지_가이드.md`
5. `03_Code/scripts/run_nonparametric_analysis.py`
6. `05_Outputs/nonparametric_analysis_walkthrough.md`

## 참고

- `main.py`는 현재 기본 FastAPI 스켈레톤입니다.
- 실질적인 비모수 분석 파이프라인은 `03_Code/` 기준으로 운영합니다.
- macOS에서 matplotlib 캐시 경고가 나면 `MPLCONFIGDIR=/tmp/matplotlib`를 붙여 실행하면 됩니다.
