# Phase 3: 코드 구조 개선 실행 계획

**작성일**: 2024-02-14
**현재 상태**: Phase 1, 2 완료
**Phase 3 상태**: 계획 단계 (실행 대기)

---

## ⚠️ 주의사항

Phase 3는 **대규모 코드 리팩토링**입니다. 다음 조건을 만족할 때 진행하는 것을 권장합니다:

- ✅ Phase 1, 2가 완료되고 안정화됨
- ✅ 현재 코드가 정상 동작함을 확인
- ✅ 전체 테스트가 통과함 (`uv run pytest`)
- ✅ Git 커밋이 완료됨
- ⚠️ **팀 규모가 확대되거나, 코드 복잡도가 증가할 때**

**현재 프로젝트 상태**: 파일 6개, 함수 17개 → **리팩토링 불필요**
**권장**: 파일 10개 이상, 함수 30개 이상 시 재검토

---

## 🎯 Phase 3 목표

### 현재 구조

```
03_Code/src/nonparametric_analysis/
└── analysis/
    ├── __init__.py
    ├── nonparametric_methods.py    (모든 분석 함수 - 약 800줄)
    ├── integrity_checks.py
    ├── sample_data.py
    ├── utils.py
    └── visualizations.py
```

**문제점**:
- `nonparametric_methods.py`가 모든 분석 함수 포함 (단일 파일 800줄)
- 카테고리별 분리 없음
- 함수 찾기 어려움

### 개선안 구조

```
03_Code/src/nonparametric_analysis/
├── core/
│   ├── __init__.py
│   ├── single_variable.py         # 정규성, 런, 추세, 변곡점, PELT
│   ├── group_comparison.py        # Mann-Whitney, K-S, Wilcoxon, Sign, Kruskal, Friedman
│   ├── correlation.py             # Spearman Matrix, Kendall, Distance
│   └── resampling.py              # Bootstrap, Permutation
├── visualization/
│   ├── __init__.py
│   ├── plots.py                   # 개별 플롯 함수들
│   └── setup.py                   # 폰트 설정 (기존 visualizations.py)
├── reporting/
│   ├── __init__.py
│   ├── templates.py               # 보고서 템플릿
│   └── generator.py               # 보고서 자동 생성
├── utils/
│   ├── __init__.py
│   ├── integrity.py               # 기존 integrity_checks.py 이동
│   ├── stats.py                   # 기존 utils.py 이동
│   └── sample.py                  # 기존 sample_data.py 이동
└── __init__.py                    # 패키지 진입점
```

**장점**:
1. 관심사 분리 (Separation of Concerns)
2. 파일당 200줄 이하로 유지
3. 테스트 작성 용이
4. 새 기능 추가 시 명확한 위치
5. import 경로 명확화

---

## 📋 실행 단계

### Step 1: 준비 작업

```bash
# 1. Git 브랜치 생성
git checkout -b refactor/phase3-structure

# 2. 백업 생성
cp -r 03_Code/src/nonparametric_analysis 03_Code/src/nonparametric_analysis_backup

# 3. 테스트 실행 (기준선)
uv run pytest > test_before_refactor.log
```

### Step 2: 새 디렉토리 구조 생성

```bash
cd 03_Code/src/nonparametric_analysis

mkdir -p core visualization reporting utils

# __init__.py 파일 생성
touch core/__init__.py visualization/__init__.py reporting/__init__.py utils/__init__.py
```

### Step 3: 파일 분리 및 이동

#### 3.1 core/ 모듈 분리

**`core/single_variable.py`** 이동 대상:
- `test_normality()`
- `runs_test_analysis()`
- `mann_kendall_test()`
- `pettitt_test()`
- `detect_changepoints_pelt()`

**`core/group_comparison.py`** 이동 대상:
- `mann_whitney_test()`
- `ks_test()`
- `wilcoxon_paired_test()`
- `sign_test()`
- `kruskal_wallis_test()`
- `friedman_test()`

**`core/correlation.py`** 이동 대상:
- `correlation_matrix_nonparametric()`
- `kendall_corr()`
- `distance_correlation()`

**`core/resampling.py`** 이동 대상:
- `bootstrap_ci()`
- `permutation_test()`

#### 3.2 utils/ 모듈 이동

```bash
mv analysis/integrity_checks.py utils/integrity.py
mv analysis/utils.py utils/stats.py
mv analysis/sample_data.py utils/sample.py
```

#### 3.3 visualization/ 모듈 분리

```bash
mv analysis/visualizations.py visualization/setup.py
# 플롯 함수들을 visualization/plots.py로 분리 (필요 시)
```

### Step 4: Import 경로 업데이트

**변경 전**:
```python
from nonparametric_analysis.analysis import nonparametric_methods as np_methods
```

**변경 후**:
```python
from nonparametric_analysis.core import single_variable
from nonparametric_analysis.core import group_comparison
from nonparametric_analysis.core import correlation
from nonparametric_analysis.core import resampling
```

**또는 패키지 레벨 export**:
```python
# nonparametric_analysis/__init__.py
from .core.single_variable import *
from .core.group_comparison import *
from .core.correlation import *
from .core.resampling import *

# 사용자 코드는 변경 불필요
from nonparametric_analysis import test_normality
```

### Step 5: 테스트 업데이트

```bash
# tests/ 폴더의 import 문 모두 업데이트
# 스크립트들의 import 문 업데이트
# 노트북의 import 문 업데이트
```

### Step 6: 검증

```bash
# 1. 테스트 실행
uv run pytest

# 2. 스크립트 실행 확인
uv run python 03_Code/scripts/run_nonparametric_analysis.py \
  --input 02_Data/sample_nonparametric.csv \
  --output 05_Outputs/phase3_test

# 3. 노트북 실행 확인
# Jupyter에서 nonparametric_analysis_final.ipynb 전체 실행

# 4. 결과 비교
diff test_before_refactor.log test_after_refactor.log
```

### Step 7: 완료 및 병합

```bash
# 1. 변경사항 커밋
git add .
git commit -m "refactor: Phase 3 코드 구조 개선

- 분석 함수 카테고리별 모듈 분리
- utils, visualization 모듈 재구성
- import 경로 업데이트
- 모든 테스트 통과 확인
"

# 2. 메인 브랜치로 병합
git checkout main
git merge refactor/phase3-structure

# 3. 백업 폴더 제거
rm -rf 03_Code/src/nonparametric_analysis_backup
```

---

## 📊 예상 작업량

| 단계 | 예상 시간 | 난이도 |
|------|----------|--------|
| Step 1: 준비 | 10분 | 쉬움 |
| Step 2: 디렉토리 생성 | 5분 | 쉬움 |
| Step 3: 파일 분리 | 2시간 | 중간 |
| Step 4: Import 업데이트 | 1시간 | 중간 |
| Step 5: 테스트 업데이트 | 1시간 | 중간 |
| Step 6: 검증 | 30분 | 중간 |
| Step 7: 완료 | 15분 | 쉬움 |
| **합계** | **약 5시간** | **중간** |

---

## ⚡ 빠른 시작 (자동화 스크립트)

### 자동 리팩토링 스크립트

```bash
# /tmp/phase3_refactor.sh 생성 및 실행
# (별도 제공 예정)
```

**주의**: 자동화 스크립트는 검토 후 사용하세요.

---

## 🤔 Phase 3 실행 판단 기준

### ✅ **즉시 실행 권장 (다음 경우)**

- [ ] 팀원 2명 이상 추가됨
- [ ] 새 분석 함수 5개 이상 추가 예정
- [ ] 코드 리뷰 시 파일 찾기 어려움 호소
- [ ] 테스트 작성 시 혼란 발생

### ⏸️ **보류 권장 (현재 상태)**

- [x] 혼자 개발 중
- [x] 파일 개수 10개 미만
- [x] 현재 구조로 충분히 작동함
- [x] 리팩토링 시간 투자 대비 효과 미미

---

## 📌 권장사항

**현재**: Phase 3 보류
**이유**:
1. 현재 파일 구조가 충분히 관리 가능 (6개 파일)
2. 팀 규모가 작음 (1인 개발)
3. 기능 추가 계획이 명확하지 않음

**재검토 시점**:
- 파일 개수 10개 이상 시
- 팀 규모 2인 이상 시
- 새 분석 함수 10개 이상 추가 시

---

## 📖 참고 자료

- [Refactoring: Improving the Design of Existing Code](https://martinfowler.com/books/refactoring.html)
- [Python Application Layouts](https://realpython.com/python-application-layouts/)
- [The Pragmatic Programmer](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/)

---

**결론**: Phase 3는 현재 보류하고, 필요 시 재검토하는 것을 권장합니다.
