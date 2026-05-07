import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app
from app.database import get_db


@pytest.fixture
def client():
    return TestClient(app)


class TestHealthEndpoint:
    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["version"] == "1.0.0"

    def test_health_detail(self, client):
        with patch(
            "app.database.async_session.execute", new_callable=AsyncMock
        ) as mock_execute:
            mock_execute.return_value.scalar.one_or_none.return_value = 1
            response = client.get("/health/detail")
            assert response.status_code == 200
            data = response.json()
            assert "database" in data
            assert data["database"] == "connected"
