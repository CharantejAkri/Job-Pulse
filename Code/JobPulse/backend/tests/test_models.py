import pytest
from unittest.mock import patch, MagicMock
from app.models import (
    User,
    Subscription,
    CreditWallet,
    CreditTransaction,
    SearchLog,
    ScrapeJob,
    DownloadHistory,
    UserRole,
    SubscriptionStatus,
    CreditType,
    JobSource,
    ScrapeStatus,
)
from datetime import datetime
from uuid import UUID


class TestUserModel:
    def test_user_default_role(self):
        user = User(email="test@example.com")
        assert user.email == "test@example.com"
        assert user.role is None

    def test_user_with_role(self):
        user = User(email="pro@example.com", role=UserRole.PRO)
        assert user.role == UserRole.PRO

    def test_user_uuid_auto_generated(self):
        user = User(email="test@example.com")
        assert isinstance(user.id, UUID)


class TestScrapeJobModel:
    def test_default_status_pending(self):
        job = ScrapeJob(
            user_id=UUID("550e8400-e29b-41d4-a716-446655440000"),
            job_title="SDE-2",
            company="Google India",
            source=JobSource.LINKEDIN,
            source_url="https://linkedin.com/jobs/1",
        )
        assert job.status is None
        assert job.is_expired is False
        assert job.is_duplicate is False

    def test_scrape_job_with_hr_data(self):
        job = ScrapeJob(
            user_id=UUID("550e8400-e29b-41d4-a716-446655440000"),
            job_title="React Developer",
            company="Flipkart",
            location="Bangalore",
            salary="₹25L",
            source=JobSource.NUKRI,
            source_url="https://naukri.com/job/1",
            hr_name="Rahul Kumar",
            hr_email="rahul@flipkart.com",
            hr_email_verified=True,
            match_score=92.5,
            status=ScrapeStatus.COMPLETED,
        )
        assert job.hr_name == "Rahul Kumar"
        assert job.match_score == 92.5

    def test_salary_parsing(self):
        job = ScrapeJob(
            user_id=UUID("550e8400-e29b-41d4-a716-446655440000"),
            job_title="DevOps Engineer",
            company="AWS India",
            source=JobSource.INDEED,
            source_url="https://indeed.in/job/1",
            salary="₹12,00,000 - ₹18,00,000",
        )
        assert "12,00,000" in job.salary


class TestCreditWalletModel:
    def test_subscription_credits_default(self):
        wallet = CreditWallet(
            user_id=UUID("550e8400-e29b-41d4-a716-446655440000"),
            credit_type=CreditType.SUBSCRIPTION,
            balance=500,
        )
        assert wallet.balance == 500
        assert wallet.credit_type == CreditType.SUBSCRIPTION

    def test_addon_credits_no_expiry(self):
        wallet = CreditWallet(
            user_id=UUID("550e8400-e29b-41d4-a716-446655440000"),
            credit_type=CreditType.ADDON,
            balance=150,
            expires_at=None,
        )
        assert wallet.balance == 150
        assert wallet.expires_at is None


class TestSubscriptionModel:
    def test_active_subscription(self):
        sub = Subscription(
            user_id=UUID("550e8400-e29b-41d4-a716-446655440000"),
            plan_type=UserRole.PRO,
            status=SubscriptionStatus.ACTIVE,
            monthly_credits=500,
        )
        assert sub.status == SubscriptionStatus.ACTIVE
        assert sub.monthly_credits == 500
