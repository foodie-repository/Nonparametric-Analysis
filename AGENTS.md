# AGENTS.md

이 문서는 이 저장소에서 작업하는 코드 에이전트를 위한 운영 가이드입니다.

> **🔧 문서 용도**: 개발자를 위한 기술 문서
> - 개발 규칙, 테스트 원칙, 체크리스트 제공
> - 기술적 근거 및 베스트 프랙티스 명시
> - Docker 배포 등 실무 주의사항 포함
>
> **프로젝트 개요가 궁금하다면**: [README.md](README.md)를 먼저 읽으세요.
> **AI 에이전트라면**: [CLAUDE.md](CLAUDE.md)를 참고하세요.

## 1) 프로젝트 목적

- 프로젝트명: `nonparametric-analysis`
- 목표: 비모수 데이터 분석 기능을 제공하는 FastAPI 기반 백엔드(향후 React 프론트엔드 연동)
- 현재 상태: 기본 API(`main.py`)와 테스트(`tests/test_main.py`)가 구성된 초기 단계

## 2) 기술 스택 및 환경

- Python `>=3.11`
- FastAPI, SQLAlchemy, Pydantic
- 패키지/실행 도구: `uv` (pip 대신 사용)
- 테스트: `pytest`

## 3) 필수 개발 명령

```bash
# 의존성 설치 (배포용 - 앱 실행에 필요한 것만)
uv sync

# 개발 의존성 포함 설치 (개발자용 - 테스트/린트 도구 포함)
uv sync --extra dev

# 개발 서버 실행
uv run uvicorn main:app --reload

# 테스트 실행
uv run pytest
```

### 의존성 분류 기준

**일반 의존성** (`[project.dependencies]`):
- 앱 실행 시 import되는 모든 패키지
- 예: `fastapi`, `sqlalchemy`, `pydantic`, `numpy`, `scipy`
- 배포 환경(Docker, 프로덕션 서버)에 반드시 포함

**개발 의존성** (`[project.optional-dependencies.dev]`):
- 개발/테스트/린트 도구
- 예: `pytest`, `pytest-cov`, `black`, `mypy`, `ruff`
- 배포 환경에서 제외 → 용량 절약, 보안 위험 감소, 배포 속도 향상

**Docker 배포 시 주의:**
```dockerfile
# ❌ 잘못된 예 (개발 도구까지 설치)
RUN uv sync --extra dev

# ✅ 올바른 예 (앱 실행에 필요한 것만)
RUN uv sync
```

## 4) 디렉터리 기준

- `main.py`: FastAPI 앱 엔트리포인트
- `03_Code/src/nonparametric_analysis/`: 핵심 분석 패키지
  - `core/`: 분석 함수 (single_variable, group_comparison, correlation, resampling)
  - `utils/`: 통계 헬퍼, 정합성 검사, 샘플 데이터 생성
  - `visualization/`: 시각화 설정 (한글 폰트)
  - `analysis/`: 기존 import 호환용 래퍼
- `02_Data/`: 샘플 데이터 + 데이터 준비 가이드
  - `데이터_준비_가이드.md`: 비개발자용 데이터 입력 안내
- `03_Code/scripts/`: 실행 스크립트 (분석 파이프라인, 데이터 생성)
- `04_Notebooks/`: Jupyter 노트북 (분석 + 해석 가이드)
  - `nonparametric_analysis_template.ipynb`: 설정 셀 기반 분석 템플릿
  - `nonparametric_analysis_final.ipynb`: 샘플 데이터 참고용 노트북
- `tests/`: 테스트 코드
- `pyproject.toml`: 의존성/빌드/pytest 설정

새 기능은 가능하면 `main.py`에 직접 누적하지 말고 `03_Code/src/nonparametric_analysis/` 내부 모듈로 분리한 뒤 라우터에서 연결합니다.

## 5) 코드 작성 규칙

- Python 스타일: PEP 8 준수
- 네이밍: 함수/변수 `snake_case`, 클래스 `PascalCase`, 상수 `UPPER_SNAKE_CASE`
- 타입 힌트 적극 사용
- API 입출력은 Pydantic 스키마로 명시
- 사용자/문서 노출 설명은 한국어 우선 사용

## 6) 비모수 분석 도메인 규칙

- 통계 함수는 가능한 순수 함수 형태로 작성하여 재사용성과 테스트 용이성 확보
- 입력 데이터 전처리(결측치, NaN, 길이 불일치, 빈 샘플) 정책을 명확히 코드로 표현
- 검정 함수는 최소한 다음을 명시:
  - 가설(H0/H1)
  - 검정 통계량 정의
  - p-value 계산 방식(또는 근사 방식)
  - 유의수준 해석 기준
- 재현성이 필요한 로직은 random seed 제어 경로 제공

## 7) 테스트 원칙

- 변경 사항마다 테스트를 함께 추가/수정
- API 엔드포인트는 `fastapi.testclient.TestClient` 기반 테스트 유지
- 새 분석 로직은 정상 케이스 + 경계/에러 케이스를 모두 포함
- 최소 실행 기준: `uv run pytest` 통과

## 8) 변경 전 확인 체크리스트

1. 의존성 추가가 정말 필요한지 검토했는가
2. 비즈니스 로직이 `main.py`에 과도하게 결합되지 않았는가
3. 타입 힌트/스키마/검증 로직이 충분한가
4. 테스트가 추가되었고 전체 테스트가 통과하는가
5. README 또는 환경 변수 문서 갱신이 필요한 변경인가

