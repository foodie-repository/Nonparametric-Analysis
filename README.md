# Nonparametric Analysis

비모수 통계 분석을 코드로 실행하고, 결과를 시각화/보고서 형태로 정리하기 위한 프로젝트입니다.

현재 저장소는 `분석 스펙(01)` → `데이터(02)` → `코드(03)` → `노트북(04)` → `결과물(05)` 흐름으로 구성되어 있습니다.

## 한눈에 보기

- 분석 사양/이론/보고서/해석 가이드 문서: `01_Specs/`
- 분석 패키지 운영 매뉴얼: `01_Specs/04_비모수_분석_패키지_가이드.md`
- 일반인을 위한 결과 해석 가이드: `01_Specs/05_비모수_통계분석_결과_해석_가이드.md`
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
│   ├── 01_비모수_분석_spec.md                      # 분석 사양 정의
│   ├── 02_비모수_분석_이론가이드.md                # 이론 및 수식 설명
│   ├── 03_비모수_보고서_템플릿.md                  # 보고서 작성 템플릿
│   ├── 04_비모수_분석_패키지_가이드.md             # 패키지 사용법
│   └── 05_비모수_통계분석_결과_해석_가이드.md      # 일반인용 해석 가이드 ⭐
├── 02_Data/
│   └── sample_nonparametric.csv                    # 샘플 데이터셋
├── 03_Code/
│   ├── scripts/
│   │   ├── generate_sample_dataset.py             # 샘플 데이터 생성
│   │   ├── run_nonparametric_analysis.py          # 전체 분석 실행
│   │   └── dev/                                    # 개발/유틸리티 스크립트
│   └── src/nonparametric_analysis/analysis/
│       ├── nonparametric_methods.py               # 17종 비모수 분석 함수
│       ├── integrity_checks.py                    # 데이터 정합성 검사
│       ├── sample_data.py                         # 샘플 데이터 생성 로직
│       ├── utils.py                               # 유틸리티 함수
│       └── visualizations.py                      # 시각화 설정
├── 04_Notebooks/
│   ├── nonparametric_analysis_final.ipynb         # 최종 실행 노트북 (모든 해석 포함) ⭐
│   └── nonparametric_analysis_template.ipynb      # 분석 템플릿 노트북
├── 05_Outputs/
│   ├── nonparametric_run/                         # 스크립트 실행 결과
│   ├── notebook_demo/                             # 노트북 실행 결과
│   └── reorg_test/                                # 재구성 테스트 결과
├── 99_Archive/                                     # 레거시 문서 보관
├── tests/                                          # 테스트 코드
│   ├── test_main.py                               # API 테스트
│   ├── test_all_methods.py                        # 전체 분석 함수 테스트
│   └── test_boxplot_empty.py                      # Box plot 엣지 케이스 테스트
├── main.py                                         # FastAPI 엔트리포인트
├── pyproject.toml                                  # 프로젝트 설정 및 의존성
├── CLAUDE.md                                       # Claude Code 가이드
├── AGENTS.md                                       # 개발 가이드
└── README.md                                       # 본 문서
```

## 작업별 빠른 네비게이션

| 하고 싶은 작업 | 먼저 볼 폴더/문서 | 다음으로 볼 코드/결과 |
|---|---|---|
| **🎯 통계 비전문가용 결과 해석** | `01_Specs/05_비모수_통계분석_결과_해석_가이드.md` | `04_Notebooks/nonparametric_analysis_final.ipynb` |
| 비모수 분석 기준 파악 | `01_Specs/01_비모수_분석_spec.md` | `03_Code/src/nonparametric_analysis/analysis/nonparametric_methods.py` |
| 이론/해석 근거 확인 | `01_Specs/02_비모수_분석_이론가이드.md` | `05_Outputs/nonparametric_run/summary.csv` |
| 보고서 작성 형식 확인 | `01_Specs/03_비모수_보고서_템플릿.md` | `05_Outputs/nonparametric_run/analysis_report.md` |
| 패키지 사용법/함수 개요 확인 | `01_Specs/04_비모수_분석_패키지_가이드.md` | `03_Code/src/nonparametric_analysis/analysis/` |
| 샘플 데이터 생성 | `03_Code/scripts/generate_sample_dataset.py` | `02_Data/sample_nonparametric.csv` |
| 전체 분석 실행 | `03_Code/scripts/run_nonparametric_analysis.py` | `05_Outputs/nonparametric_run/` |
| 정합성 규칙 수정 | `03_Code/src/nonparametric_analysis/analysis/integrity_checks.py` | `05_Outputs/nonparametric_run/integrity_check.csv` |
| 추세/변곡점 로직 수정 | `03_Code/src/nonparametric_analysis/analysis/nonparametric_methods.py` | `05_Outputs/nonparametric_run/figures/*pettitt*.png`, `*mk*.png` |
| 상관/FDR 로직 수정 | `03_Code/src/nonparametric_analysis/analysis/utils.py` | `05_Outputs/nonparametric_run/correlation_pvalues_adjusted.csv` |
| **🔬 노트북 기반 탐색 분석** | `04_Notebooks/nonparametric_analysis_final.ipynb` | `05_Outputs/notebook_demo/` |
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

- `05_Outputs/nonparametric_run/summary.csv` - 분석 요약
- `05_Outputs/nonparametric_run/integrity_check.csv` - 정합성 검사 결과
- `05_Outputs/nonparametric_run/correlation_pvalues_adjusted.csv` - 상관분석 결과
- `05_Outputs/nonparametric_run/figures/*.png` - 시각화 차트들

## 노트북 실행

**추천 노트북:**
- **`04_Notebooks/nonparametric_analysis_final.ipynb`** ⭐
  - 17종 비모수 분석 전체 포함
  - 각 분석마다 **통계 비전문가를 위한 상세한 해석 가이드** 포함
  - 실무 활용 예시 및 차트 읽는 법 설명

- `04_Notebooks/nonparametric_analysis_template.ipynb`
  - 새로운 데이터로 분석 시작 시 복사해서 사용

## 테스트

```bash
# API 기본 테스트
uv run pytest tests/test_main.py

# 전체 분석 함수 테스트
uv run pytest tests/test_all_methods.py

# 모든 테스트 실행
uv run pytest
```

## 문서 읽기 순서 추천

### 📚 **통계 비전문가**

1. `01_Specs/05_비모수_통계분석_결과_해석_가이드.md` - p-value, 효과 크기 등 기본 개념
2. `04_Notebooks/nonparametric_analysis_final.ipynb` - 실제 분석 결과 + 해석
3. `01_Specs/03_비모수_보고서_템플릿.md` - 보고서 작성 예시

### 👨‍💻 **개발자/데이터 분석가**

1. `01_Specs/01_비모수_분석_spec.md` - 분석 사양 및 요구사항
2. `01_Specs/02_비모수_분석_이론가이드.md` - 통계 이론 및 수식
3. `01_Specs/04_비모수_분석_패키지_가이드.md` - 함수 API 레퍼런스
4. `03_Code/scripts/run_nonparametric_analysis.py` - 실행 예시
5. `AGENTS.md` - 개발 규칙 및 체크리스트

## 주요 기능 (17종 비모수 분석)

### 단일 변수 분석
1. 정규성 검정 (Shapiro-Wilk)
2. 런 검정 (Runs Test - 무작위성)
3. 추세 분석 (Mann-Kendall Trend)
4. 변곡점 탐지 (Pettitt Test)
5. 다중 구간 분할 (PELT)

### 그룹 비교
6. 두 독립 그룹 비교 (Mann-Whitney U)
7. 두 분포 비교 (Kolmogorov-Smirnov)
8. 짝지어진 그룹 비교 (Wilcoxon Signed Rank)
9. 부호 검정 (Sign Test)
10. 세 독립 그룹 비교 (Kruskal-Wallis)
11. 반복 측정 비교 (Friedman Test)

### 상관 관계
12. 상관 행렬 (Spearman Correlation Matrix + FDR 보정)
13. 켄달 타우 상관 (Kendall's Tau)
14. 거리 상관 (Distance Correlation - 비선형 관계)

### 리샘플링
15. 부트스트랩 신뢰구간 (Bootstrap CI)
16. 순열 검정 (Permutation Test)

### 정합성 검사
17. 데이터 무결성 검사 (결측치, 이상치, 길이 불일치 등)

## 참고

- `main.py`는 현재 기본 FastAPI 스켈레톤입니다.
- 실질적인 비모수 분석 파이프라인은 `03_Code/` 기준으로 운영합니다.
- macOS에서 matplotlib 캐시 경고가 나면 `MPLCONFIGDIR=/tmp/matplotlib`를 붙여 실행하면 됩니다.
- 개발 규칙 및 체크리스트는 `AGENTS.md`를 참조하세요.

## 최근 업데이트 (2024-02-13)

- ✅ 노트북 해석 섹션 전면 강화 (통계 비전문가용)
- ✅ `05_비모수_통계분석_결과_해석_가이드.md` 신규 추가
- ✅ 모든 분석 함수 파라미터 에러 수정 완료
- ✅ 한글 폰트 설정 개선 (macOS 지원)
