import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.api.v1.auth import get_current_user


def override_get_current_user():
    return {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "test@example.com",
        "user_metadata": {"full_name": "Test User", "role": "pro"},
        "created_at": "2026-05-07T00:00:00Z",
    }


app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.fixture
def client():
    return TestClient(app)


class TestCreditsAPI:
    @patch("app.database.async_session.execute", new_callable=AsyncMock)
    def test_get_credit_balance(self, mock_execute, client):
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_execute.return_value = mock_result

        response = client.get("/api/v1/credits/balance")
        assert response.status_code == 200
        data = response.json()
        assert "subscription_credits" in data
        assert "total_credits" in data

    def test_topup_invalid_pack(self, client):
        response = client.post(
            "/api/v1/credits/topup",
            json={
                "pack_type": "invalid_pack",
                "razorpay_payment_id": "pay_test",
            },
        )
        assert response.status_code == 400
        assert "Invalid pack type" in response.json()["detail"]

    def test_topup_booster(self, client):
        with patch("razorpay.Client.order.create") as mock_order:
            mock_order.return_value = {
                "id": "order_test",
                "amount": 59900,
                "currency": "INR",
            }
            response = client.post(
                "/api/v1/credits/topup",
                json={
                    "pack_type": "booster_150",
                    "razorpay_payment_id": "pay_test",
                },
            )
            assert response.status_code == 200
            data = response.json()
            assert data["credits"] == 150
            assert data["amount"] == 59900
            assert data["currency"] == "INR"
