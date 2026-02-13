# Changelog

이 파일은 Nonparametric-Analysis 프로젝트의 주요 변경사항을 기록합니다.

형식은 [Keep a Changelog](https://keepachangelog.com/ko/1.0.0/)를 따르며,
버전 관리는 [Semantic Versioning](https://semver.org/lang/ko/)을 준수합니다.

## [Unreleased]

---

## [0.2.0] - 2024-02-14

### Added
- 📚 `01_Specs/README.md` - Specs 문서 가이드 추가
- 📋 `CHANGELOG.md` - 변경사항 추적 문서 추가
- 📖 `05_비모수_통계분석_결과_해석_가이드.md` - 일반인용 결과 해석 가이드
- 📓 노트북 해석 섹션 전면 강화 (17개 분석 모두)
- 🗂️ `.gitignore` - Python, Jupyter, uv 관련 파일 제외

### Changed
- 🏗️ **Phase 3: 패키지 구조 리팩토링 완료**
  - `nonparametric_methods.py` 단일 파일 → 카테고리별 4개 모듈로 분리
    - `core/single_variable.py` - 정규성, 런, 추세, 변곡점, PELT
    - `core/group_comparison.py` - Mann-Whitney, K-S, Wilcoxon, Kruskal, Friedman
    - `core/correlation.py` - Spearman, Kendall, Distance 상관분석
    - `core/resampling.py` - Bootstrap, Permutation
  - 유틸리티 모듈 재구성 (`utils/stats.py`, `utils/integrity.py`, `utils/sample.py`)
  - 시각화 모듈 분리 (`visualization/setup.py`)
  - 기존 `from nonparametric_analysis.analysis import ...` 호환성 유지
- 🏗️ Phase 1, 2: 프로젝트 구조 개선
  - `outputs/` → `05_Outputs/`로 통합
  - 루트 스크립트 파일 → `03_Code/scripts/dev/`로 이동
  - 테스트 파일 → `tests/`로 통합
- 📝 `README.md` 전면 개편
  - 최신 패키지 구조 반영
  - 17종 비모수 분석 목록 추가
  - 대상 독자별 읽기 순서 추가
  - 패키지 Import 방법 가이드 추가

### Removed
- 🗑️ 불필요한 파일 제거
  - `README_OLD.md` (구버전 README)
  - `PHASE3_PLAN.md`, `프로젝트_구조_개선_제안.md` (완료된 계획 문서)
  - `__pycache__/`, `test_before_refactor.log` (임시 파일)

### Fixed
- 🐛 모든 분석 함수 파라미터 오류 수정 (7개 함수)
  - Mann-Whitney: `name_a/name_b` → `name1/name2`
  - K-S Test: `name_a/name_b` → `name1/name2`
  - Wilcoxon: `name_a/name_b` → `name`
  - Friedman: `group_names` → `condition_names`
  - Distance Correlation: `'correlation'` → `'dcor'`
  - Permutation Test: 람다 함수 → 단일 통계 함수
- 🎨 한글 폰트 설정 개선 (macOS)
  - AppleSDGothicNeo-Regular 우선 선택
  - 폰트 fallback 체인 추가
- 🧪 테스트 코드 수정 (함수명, 반환 타입 맞춤)

---

## [0.1.0] - 2024-02-13

### Added
- 🎉 초기 프로젝트 구조 생성
- 📊 17종 비모수 분석 함수 구현
  - 단일 변수 분석 (5종)
  - 그룹 비교 (6종)
  - 상관 관계 (3종)
  - 리샘플링 (2종)
  - 정합성 검사 (1종)
- 📁 번호 기반 폴더 구조
  - `01_Specs/` - 분석 사양 및 가이드 문서
  - `02_Data/` - 샘플 데이터셋
  - `03_Code/` - 핵심 분석 코드
  - `04_Notebooks/` - Jupyter 노트북
  - `05_Outputs/` - 분석 결과물
  - `99_Archive/` - 레거시 문서
- 📖 핵심 문서 작성
  - `01_비모수_분석_spec.md`
  - `02_비모수_분석_이론가이드.md`
  - `03_비모수_보고서_템플릿.md`
  - `04_비모수_분석_패키지_가이드.md`
- 🚀 FastAPI 기반 API 스켈레톤
- 🧪 pytest 기반 테스트 환경
- 📦 uv 패키지 매니저 채택

### Technical
- Python 3.11+ 지원
- 의존성: scipy, numpy, pandas, matplotlib, seaborn
- 특수 라이브러리: pymannkendall, ruptures, dcor

---

## 변경 유형 설명

- `Added` - 새로운 기능
- `Changed` - 기존 기능 변경
- `Deprecated` - 곧 제거될 기능
- `Removed` - 제거된 기능
- `Fixed` - 버그 수정
- `Security` - 보안 관련 수정

---

## 다음 계획 (Future)

### v0.3.0 (예정)
- [ ] React 프론트엔드 통합
- [ ] API 엔드포인트 확장
- [ ] 추가 비모수 검정 방법
  - Mood's Median Test
  - Jonckheere-Terpstra Test

### v0.4.0 (예정)
- [ ] 사용자 인터페이스 개선
- [ ] 보고서 자동 생성 기능
- [ ] 다국어 지원 (영어)
- [ ] 성능 최적화

---

**참고**: 이 프로젝트는 활발히 개발 중이며, 버전 1.0.0 이전에는 API 변경이 있을 수 있습니다.
