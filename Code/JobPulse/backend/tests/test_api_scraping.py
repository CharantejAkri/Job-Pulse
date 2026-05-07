import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.api.v1.auth import get_current_user

app.dependency_overrides[get_current_user] = lambda: {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "test@example.com",
    "user_metadata": {"full_name": "Test User", "role": "pro"},
    "created_at": "2026-05-07T00:00:00Z",
}


@pytest.fixture
def client():
    return TestClient(app)


class TestScrapingAPI:
    @patch("app.api.v1.scraping.start_scrape_task.delay")
    def test_start_scrape(self, mock_task, client):
        mock_task.return_value.id = "celery-task-123"

        response = client.post(
            "/api/v1/scraping/start",
            json={
                "job_title": "React Developer",
                "location": "Mumbai",
                "sources": ["linkedin", "indeed"],
                "date_posted": "past_24h",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["task_id"] == "celery-task-123"
        assert "estimated_credits" in data

    def test_start_scrape_no_sources(self, client):
        response = client.post(
            "/api/v1/scraping/start",
            json={
                "job_title": "React Developer",
                "sources": [],
            },
        )
        assert response.status_code == 400
        assert "At least one source" in response.json()["detail"]

    def test_start_scrape_no_title(self, client):
        response = client.post(
            "/api/v1/scraping/start",
            json={
                "sources": ["linkedin"],
            },
        )
        assert response.status_code == 422

    @patch("app.api.v1.scraping.celery_app.AsyncResult")
    def test_get_task_status(self, mock_async_result, client):
        mock_result = MagicMock()
        mock_result.status = "PENDING"
        mock_result.ready.return_value = False
        mock_async_result.return_value = mock_result

        response = client.get("/api/v1/scraping/tasks/some-task-id")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "PENDING"

    @patch("app.api.v1.scraping.celery_app.AsyncResult")
    def test_get_task_status_completed(self, mock_async_result, client):
        mock_result = MagicMock()
        mock_result.status = "SUCCESS"
        mock_result.ready.return_value = True
        mock_result.result = {"status": "completed", "job_count": 25}
        mock_async_result.return_value = mock_result

        response = client.get("/api/v1/scraping/tasks/some-task-id")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SUCCESS"
        assert data["result"]["job_count"] == 25
