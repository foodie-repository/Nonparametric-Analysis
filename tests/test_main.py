"""FastAPI 애플리케이션 테스트"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    """루트 엔드포인트 테스트"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Nonparametric Analysis API"}


def test_health_check():
    """헬스 체크 엔드포인트 테스트"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
