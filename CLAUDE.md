# CLAUDE.md

이 파일은 Claude Code (claude.ai/code)가 이 저장소에서 작업할 때 참고하는 가이드입니다.

> **📘 문서 용도**: AI 에이전트를 위한 기술 문서
> - 정확한 개념 정의 및 명령어 가이드 제공
> - 프로젝트 아키텍처 및 개발 규칙 명시
> - 사람이 읽기보다는 AI가 이해하기 쉬운 형식으로 작성됨
>
> **일반 사용자라면**: [README.md](README.md)를 먼저 읽으세요.
> **개발자라면**: [AGENTS.md](AGENTS.md)도 함께 참고하세요.

## 프로젝트 개요

**Nonparametric Analysis**는 비모수 통계 분석을 위한 FastAPI + React 웹 서비스입니다. 현재 FastAPI 기반 백엔드 API가 구현되어 있으며, React 프론트엔드는 계획 단계입니다.

## 기술 스택

- **Python 3.11+** - 백엔드 언어
- **FastAPI** - 고성능 웹 프레임워크 (자동 OpenAPI 문서화 지원)
- **SQLAlchemy** - ORM (데이터베이스 작업)
- **Pydantic** - 데이터 검증 및 설정 관리
- **uv** - 최신 고속 Python 패키지 관리자 (pip/poetry 대체)
- **pytest** - 테스트 프레임워크 (비동기 지원)

## 개발 명령어

### 패키지 관리 (uv)

이 프로젝트는 **pip 대신 uv를 사용**합니다. 모든 패키지 작업은 uv로 수행해야 합니다:

```bash
# 모든 의존성 설치 (배포용)
uv sync

# 개발 의존성 포함 설치 (개발자용)
uv sync --extra dev

# 새 패키지 추가
uv add <패키지명>

# 개발 의존성 추가
uv add --dev <패키지명>

# 패키지 제거
uv remove <패키지명>

# 가상환경에서 명령 실행
uv run <명령어>
```

#### 일반 의존성 vs 개발 의존성

**일반 의존성 (Production Dependencies)**
- 앱이 실제로 실행될 때 필요한 패키지 (예: `fastapi`, `sqlalchemy`, `pydantic`)
- 배포 서버에 반드시 포함되어야 함
- `uv add <패키지명>`으로 추가

**개발 의존성 (Development Dependencies)**
- 개발자가 개발/테스트할 때만 필요한 패키지 (예: `pytest`, `black`, `mypy`)
- 배포 서버에는 불필요 (용량 절약, 보안 향상, 배포 속도 개선)
- `uv add --dev <패키지명>`으로 추가

**설치 명령어 선택 가이드:**
- **개발자 본인**: `uv sync --extra dev` (코드 수정, 테스트 실행 필요)
- **배포 서버/일반 사용자**: `uv sync` (앱 실행만 필요)

### 애플리케이션 실행

```bash
# 개발 서버 시작 (자동 리로드)
uv run uvicorn main:app --reload

# 커스텀 호스트/포트로 시작
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API 접근 주소:
- 메인 API: `http://localhost:8000`
- 대화형 API 문서 (Swagger): `http://localhost:8000/docs`
- 대체 API 문서 (ReDoc): `http://localhost:8000/redoc`

### 테스트

```bash
# 모든 테스트 실행
uv run pytest

# 상세 출력으로 테스트 실행
uv run pytest -v

# 특정 테스트 파일 실행
uv run pytest tests/test_main.py

# 커버리지와 함께 실행
uv run pytest --cov=src/nonparametric_analysis
```

### 환경 설정

1. 환경 변수 템플릿 복사:
   ```bash
   cp .env.example .env
   ```

2. `.env` 파일을 편집하여 설정:
   - `DATABASE_URL` - 데이터베이스 연결 문자열 (기본값: SQLite)
   - `SECRET_KEY` - 보안 기능용 비밀 키
   - `API_V1_PREFIX` - API 버전 접두사

## 프로젝트 아키텍처

### 디렉토리 구조

```
.
├── main.py                       # FastAPI 애플리케이션 진입점
├── src/
│   └── nonparametric_analysis/  # 메인 애플리케이션 패키지
│       └── __init__.py          # 패키지 버전 및 메타데이터
├── tests/                       # 테스트 파일
│   ├── __init__.py
│   └── test_main.py            # API 엔드포인트 테스트
├── pyproject.toml              # 프로젝트 설정 및 의존성
├── uv.lock                     # 잠긴 의존성 버전
├── .env.example                # 환경 변수 템플릿
└── .venv/                      # 가상환경 (uv가 자동 생성)
```

### 애플리케이션 구조

- **main.py**: FastAPI 애플리케이션 진입점
  - title, description, version이 포함된 FastAPI 앱 인스턴스
  - React 프론트엔드(`http://localhost:3000`)를 위한 CORS 미들웨어 설정
  - 기본 엔드포인트: `/` (루트), `/health` (헬스 체크)

- **src/nonparametric_analysis/**: 메인 애플리케이션 패키지
  - Python의 src-layout 패턴을 따름 (패키지 격리 개선)
  - 현재는 최소 구성이며, 비즈니스 로직 모듈 추가 예정

- **tests/**: pytest를 사용한 테스트 스위트
  - 엔드포인트 테스트를 위해 FastAPI의 `TestClient` 사용
  - `pytest-asyncio`로 비동기 테스트 지원

### 주요 아키텍처 특징

1. **src-layout 패턴**: 패키지가 `src/` 디렉토리 안에 위치
   - 작업 디렉토리에서 실수로 임포트하는 것을 방지
   - 테스트가 설치된 패키지를 대상으로 실행됨을 보장
   - Python 패키지의 권장 구조

2. **CORS 설정**: 현재 `http://localhost:3000`에서의 요청 허용
   - 로컬 React 개발을 위한 설정
   - 프로덕션에서는 특정 origin으로 업데이트 필요

3. **테스트 전략**:
   - FastAPI의 `TestClient` 사용 (실제 서버 없이 앱 실행)
   - FastAPI가 비동기를 사용하지만 테스트는 동기식
   - `main` 모듈에서 직접 임포트

4. **빌드 시스템**: `hatchling`을 빌드 백엔드로 사용
   - 현대적이고 표준 준수 빌드 시스템
   - `src/nonparametric_analysis`를 wheel로 패키징하도록 설정

## 코딩 스타일 및 컨벤션

- **PEP 8**: Python 공식 스타일 가이드 준수
- **네이밍**:
  - 함수/변수: `snake_case`
  - 클래스: `PascalCase`
  - 상수: `UPPER_SNAKE_CASE`
- **Docstring**: 사용자 대면 설명은 한국어 사용
- **타입 힌트**: 요청/응답 스키마에 Pydantic 모델 사용
- **커밋 메시지**: Conventional Commits 형식 준수

## 프론트엔드 통합 (계획)

React 프론트엔드 통합을 위한 설계:
- 프론트엔드는 `frontend/` 디렉토리에 위치 예정
- 백엔드 CORS는 `localhost:3000`에 미리 설정됨
- API 엔드포인트는 REST 규칙을 따라야 함
- 타입 안정성을 위해 React + TypeScript 사용 권장

## 데이터베이스

현재 SQLite로 설정되어 있음(`.env.example` 참조), SQLAlchemy는 다음을 지원:
- PostgreSQL (프로덕션 권장)
- MySQL/MariaDB
- SQLite (개발/테스트용)

데이터베이스 백엔드 변경은 `.env`의 `DATABASE_URL`을 수정하면 됩니다.

## 중요 참고사항

- **uv 우선**: 모든 패키지 작업은 pip 대신 uv 사용
- **FastAPI 자동 문서화**: `/docs`와 `/redoc`에서 자동 생성된 API 문서 확인 가능
- **비동기 지원**: FastAPI는 비동기 엔드포인트를 지원하므로 `async/await` 활용 권장
- **환경 변수**: 민감한 정보는 반드시 `.env` 파일에 저장하고 `.gitignore`로 관리
