import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def mock_db():
    """Mock database session for unit tests."""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def fake_user():
    """Returns a fake authenticated user payload."""
    return {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "test@example.com",
        "user_metadata": {
            "full_name": "Test User",
            "role": "pro",
        },
        "created_at": "2026-05-07T00:00:00Z",
    }


@pytest.fixture
def fake_job_data():
    """Returns fake scraped job data."""
    return {
        "job_title": "React Developer",
        "company": "TechCorp India",
        "location": "Mumbai",
        "salary": "₹15,00,000 - ₹20,00,000",
        "source": "linkedin",
        "source_url": "https://linkedin.com/jobs/view/123",
        "description": "We are looking for a React Developer with 3+ years of experience.",
        "hr_name": "Priya Sharma",
        "hr_email": "priya@techcorp.com",
        "hr_email_verified": True,
        "match_score": 85.0,
    }


@pytest.fixture
def fake_credit_balance():
    """Returns a fake credit balance response."""
    return {
        "subscription_credits": 450,
        "addon_credits": 150,
        "total_credits": 600,
    }
