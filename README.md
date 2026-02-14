# Nonparametric Analysis

비모수 통계 분석을 코드로 실행하고, 결과를 시각화/보고서 형태로 정리하기 위한 프로젝트입니다.

현재 저장소는 `분석 스펙(01)` → `데이터(02)` → `실행 스크립트(03)` → `노트북(04)` → `결과물(05)` 흐름으로 구성되어 있습니다.

## 한눈에 보기

- 분석 사양/이론/보고서/해석 가이드 문서: `01_Specs/`
- 일반인을 위한 결과 해석 가이드: `01_Specs/05_비모수_통계분석_결과_해석_가이드.md`
- 샘플 및 입력 데이터: `02_Data/`
- **새 데이터로 분석 시작하기**: `02_Data/데이터_준비_가이드.md`
- 실행 스크립트: `03_Code/scripts/`
- 핵심 분석 패키지: `03_Code/src/nonparametric_analysis/`
- 탐색/시각화 노트북: `04_Notebooks/`
- 실행 결과 및 리포트: `05_Outputs/`
- 레거시/보관 문서: `99_Archive/`
- API 스켈레톤(FastAPI): `main.py`

## 프로젝트 구조

```text
.
├── 01_Specs/
│   ├── 01_비모수_분석_spec.md                      # 분석 사양 정의
│   ├── 02_비모수_분석_이론가이드.md                # 이론 및 수식 설명
│   ├── 03_비모수_보고서_템플릿.md                  # 보고서 작성 템플릿
│   ├── 04_비모수_분석_패키지_가이드.md             # 패키지 사용법
│   ├── 05_비모수_통계분석_결과_해석_가이드.md      # 일반인용 해석 가이드
│   └── README.md                                   # 문서 네비게이션
├── 02_Data/
│   ├── sample_nonparametric.csv                    # 샘플 데이터셋
│   └── 데이터_준비_가이드.md                       # 데이터 입력 안내
├── 03_Code/
│   ├── scripts/
│   │   ├── generate_sample_dataset.py             # 샘플 데이터 생성
│   │   ├── run_nonparametric_analysis.py          # 전체 분석 실행
│   │   └── dev/                                    # 개발/유틸리티 스크립트
│   └── src/nonparametric_analysis/                 # 핵심 분석 패키지
│       ├── core/                                   # 분석 함수 (카테고리별 분리)
│       │   ├── single_variable.py                 #   정규성, 런, 추세, 변곡점, PELT
│       │   ├── group_comparison.py                #   Mann-Whitney, K-S, Wilcoxon, Kruskal, Friedman
│       │   ├── correlation.py                     #   Spearman, Kendall, Distance 상관분석
│       │   └── resampling.py                      #   Bootstrap, Permutation
│       ├── utils/                                  # 유틸리티
│       │   ├── stats.py                           #   통계 헬퍼 함수
│       │   ├── integrity.py                       #   데이터 정합성 검사
│       │   └── sample.py                          #   샘플 데이터 생성 로직
│       ├── visualization/
│       │   └── setup.py                           #   한글 폰트/시각화 설정
│       └── analysis/                               # 기존 import 호환용
├── 04_Notebooks/
│   ├── nonparametric_analysis_final.ipynb         # 최종 실행 노트북 (모든 해석 포함)
│   └── nonparametric_analysis_template.ipynb      # 분석 템플릿 노트북
├── 05_Outputs/
│   ├── nonparametric_run/                         # 스크립트 실행 결과
│   └── notebook_demo/                             # 노트북 실행 결과
├── 99_Archive/                                     # 레거시 문서 보관
├── tests/                                          # 테스트 코드
│   ├── test_main.py                               # API 테스트
│   ├── test_nonparametric_analysis.py             # 분석 함수 테스트
│   └── test_boxplot_empty.py                      # Box plot 엣지 케이스 테스트
├── main.py                                         # FastAPI 엔트리포인트
├── pyproject.toml                                  # 프로젝트 설정 및 의존성
├── CLAUDE.md                                       # Claude Code 가이드
├── AGENTS.md                                       # 개발 가이드
├── CHANGELOG.md                                    # 변경 이력
└── README.md                                       # 본 문서
```

## 작업별 빠른 네비게이션

| 하고 싶은 작업 | 먼저 볼 폴더/문서 | 다음으로 볼 코드/결과 |
|---|---|---|
| **내 데이터로 분석 시작** | `02_Data/데이터_준비_가이드.md` | `04_Notebooks/nonparametric_analysis_template.ipynb` |
| **통계 비전문가용 결과 해석** | `01_Specs/05_비모수_통계분석_결과_해석_가이드.md` | `04_Notebooks/nonparametric_analysis_final.ipynb` |
| 비모수 분석 기준 파악 | `01_Specs/01_비모수_분석_spec.md` | `03_Code/src/nonparametric_analysis/core/` |
| 이론/해석 근거 확인 | `01_Specs/02_비모수_분석_이론가이드.md` | `05_Outputs/nonparametric_run/summary.csv` |
| 보고서 작성 형식 확인 | `01_Specs/03_비모수_보고서_템플릿.md` | `05_Outputs/nonparametric_run/analysis_report.md` |
| 패키지 사용법/함수 개요 확인 | `01_Specs/04_비모수_분석_패키지_가이드.md` | `03_Code/src/nonparametric_analysis/core/` |
| 샘플 데이터 생성 | `03_Code/scripts/generate_sample_dataset.py` | `02_Data/sample_nonparametric.csv` |
| 전체 분석 실행 | `03_Code/scripts/run_nonparametric_analysis.py` | `05_Outputs/nonparametric_run/` |
| 정합성 규칙 수정 | `03_Code/src/nonparametric_analysis/utils/integrity.py` | `05_Outputs/nonparametric_run/integrity_check.csv` |
| 추세/변곡점 로직 수정 | `03_Code/src/nonparametric_analysis/core/single_variable.py` | `05_Outputs/nonparametric_run/figures/` |
| 상관/FDR 로직 수정 | `03_Code/src/nonparametric_analysis/core/correlation.py` | `05_Outputs/nonparametric_run/correlation_pvalues_adjusted.csv` |
| **노트북 기반 탐색 분석** | `04_Notebooks/nonparametric_analysis_final.ipynb` | `05_Outputs/notebook_demo/` |
| API 엔드포인트 작업 | `main.py` | `tests/test_main.py` |

## 사전 준비

이 프로젝트는 Python 패키지 관리자 **[uv](https://docs.astral.sh/uv/)**를 사용합니다. 최초 1회 설치가 필요합니다.

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

> **참고**: Python은 별도 설치하지 않아도 됩니다. uv가 프로젝트에 필요한 Python 3.11을 자동으로 다운로드합니다.

## 빠른 시작

```bash
# 1) 의존성 설치 (Python 자동 다운로드 포함)
#    개발자용 (코드 수정하실 분):
uv sync --extra dev

#    일반 사용자용 (앱만 실행하실 분):
uv sync
```

### 💡 의존성 설치 옵션 설명

| 대상 | 명령어 | 설치되는 패키지 |
|------|--------|-----------------|
| **개발자** (코드 수정/테스트) | `uv sync --extra dev` | fastapi, pytest, black 등 **모든 패키지** |
| **일반 사용자** (앱만 실행) | `uv sync` | fastapi, sqlalchemy 등 **실행에 필요한 것만** |

처음 시작하시는 분은 `uv sync --extra dev`로 전부 설치하는 것을 권장합니다.

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

- `05_Outputs/nonparametric_run/summary.csv` - 분석 요약
- `05_Outputs/nonparametric_run/integrity_check.csv` - 정합성 검사 결과
- `05_Outputs/nonparametric_run/correlation_pvalues_adjusted.csv` - 상관분석 결과
- `05_Outputs/nonparametric_run/figures/*.png` - 시각화 차트들

## 본인 데이터로 분석하기

**방법 A: CSV 파일 사용**
1. CSV 파일을 `02_Data/` 폴더에 넣기
2. `04_Notebooks/nonparametric_analysis_template.ipynb` 열기
3. **설정 셀 하나만 수정** (파일명, 컬럼명 입력)
4. 전체 셀 실행 → 해당되지 않는 분석은 자동 건너뜀

**방법 B: 복사/붙여넣기 (DRM 문서용)**
1. `04_Notebooks/nonparametric_analysis_template.ipynb` 열기
2. 설정 셀의 `PASTE_DATA`에 데이터 직접 붙여넣기
3. 컬럼명 설정 후 전체 셀 실행

자세한 데이터 형식은 `02_Data/데이터_준비_가이드.md`를 참고하세요.

## 노트북 실행

**추천 노트북:**
- **`04_Notebooks/nonparametric_analysis_final.ipynb`** (참고용)
  - 17종 비모수 분석 전체 포함
  - 각 분석마다 **통계 비전문가를 위한 상세한 해석 가이드** 포함
  - 실무 활용 예시 및 차트 읽는 법 설명
  - `show_result(res)` 헬퍼로 결과 요약 + 차트 자동 출력

- **`04_Notebooks/nonparametric_analysis_template.ipynb`** (실제 분석용)
  - **설정 셀 하나만 수정**하면 본인 데이터로 17종 분석 가능
  - CSV 파일 또는 **복사/붙여넣기**(DRM 문서용) 두 가지 입력 방식 지원
  - 데이터 검증 + 한국어 오류 안내 내장
  - 미설정 분석은 자동 건너뜀 (에러 없음)

## 테스트

```bash
# 모든 테스트 실행
uv run pytest

# 특정 테스트 실행
uv run pytest tests/test_main.py
uv run pytest tests/test_nonparametric_analysis.py
```

## 패키지 Import 방법

```python
# 방법 1: 패키지에서 직접 import (권장)
from nonparametric_analysis import test_normality, pettitt_test, bootstrap_ci

# 방법 2: 카테고리별 모듈에서 import
from nonparametric_analysis.core.single_variable import test_normality
from nonparametric_analysis.core.group_comparison import mann_whitney_test
from nonparametric_analysis.core.correlation import correlation_matrix_nonparametric
from nonparametric_analysis.core.resampling import bootstrap_ci

# 유틸리티 함수
from nonparametric_analysis.utils import generate_sample_dataset, adjust_pvalue_matrix_fdr
```

## 문서 읽기 순서 추천

### 통계 비전문가

1. `01_Specs/05_비모수_통계분석_결과_해석_가이드.md` - p-value, 효과 크기 등 기본 개념
2. `04_Notebooks/nonparametric_analysis_final.ipynb` - 실제 분석 결과 + 해석
3. `01_Specs/03_비모수_보고서_템플릿.md` - 보고서 작성 예시

### 개발자/데이터 분석가

1. `01_Specs/01_비모수_분석_spec.md` - 분석 사양 및 요구사항
2. `01_Specs/02_비모수_분석_이론가이드.md` - 통계 이론 및 수식
3. `01_Specs/04_비모수_분석_패키지_가이드.md` - 함수 API 레퍼런스
4. `03_Code/scripts/run_nonparametric_analysis.py` - 실행 예시
5. `AGENTS.md` - 개발 규칙 및 체크리스트

## 주요 기능 (17종 비모수 분석)

### 단일 변수 분석 (`core/single_variable.py`)
1. 정규성 검정 (Shapiro-Wilk)
2. 런 검정 (Runs Test - 무작위성)
3. 추세 분석 (Mann-Kendall Trend)
4. 변곡점 탐지 (Pettitt Test)
5. 다중 구간 분할 (PELT)

### 그룹 비교 (`core/group_comparison.py`)
6. 두 독립 그룹 비교 (Mann-Whitney U)
7. 두 분포 비교 (Kolmogorov-Smirnov)
8. 짝지어진 그룹 비교 (Wilcoxon Signed Rank)
9. 부호 검정 (Sign Test)
10. 세 독립 그룹 비교 (Kruskal-Wallis)
11. 반복 측정 비교 (Friedman Test)

### 상관 관계 (`core/correlation.py`)
12. 상관 행렬 (Spearman Correlation Matrix + FDR 보정)
13. 켄달 타우 상관 (Kendall's Tau)
14. 거리 상관 (Distance Correlation - 비선형 관계)

### 리샘플링 (`core/resampling.py`)
15. 부트스트랩 신뢰구간 (Bootstrap CI)
16. 순열 검정 (Permutation Test)

### 정합성 검사 (`utils/integrity.py`)
17. 데이터 무결성 검사 (결측치, 이상치, 길이 불일치 등)

## 참고

- `main.py`는 현재 기본 FastAPI 스켈레톤입니다.
- 실질적인 비모수 분석 파이프라인은 `03_Code/scripts/`로 실행합니다.
- macOS에서 matplotlib 캐시 경고가 나면 `MPLCONFIGDIR=/tmp/matplotlib`를 붙여 실행하면 됩니다.
- 개발 규칙 및 체크리스트는 `AGENTS.md`를 참조하세요.
- 변경 이력은 `CHANGELOG.md`를 참조하세요.

## 최근 업데이트 (2026-02-14)

- 데이터 복사/붙여넣기 지원 추가 (v0.3.1)
  - DRM 문서 등 파일 저장이 어려운 경우 `PASTE_DATA` 변수에 직접 붙여넣기 가능
  - 쉼표/탭/세미콜론 구분자 자동 인식
  - 노트북 헤딩/구조를 final 노트북과 통일 (섹션 헤더 추가, 42셀)
- 템플릿 노트북 사용성 대폭 개선 (v0.3.0)
  - **설정 셀 1개만 수정**하면 본인 데이터로 전체 분석 가능
  - 데이터 검증 + 한국어 오류 메시지 내장
  - 미설정 분석(그룹비교, 전/후 비교 등)은 자동 건너뜀
  - `02_Data/데이터_준비_가이드.md` 신규 추가
- 노트북 출력 문제 수정 (v0.2.1)
  - `matplotlib.use('Agg')` 제거 → `%matplotlib inline`으로 차트 정상 표시
  - 모든 분석 셀에 `show_result()` 헬퍼 추가
- 코드 구조 리팩토링 완료 (v0.2.0)
  - 분석 함수 카테고리별 모듈 분리 (`core/` 4개 모듈)
  - 유틸리티/시각화 모듈 재구성 (`utils/`, `visualization/`)
