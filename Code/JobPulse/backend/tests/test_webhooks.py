import pytest
import json
import hmac
import hashlib
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app

WEBHOOK_SECRET = "test_webhook_secret"


def sign_body(body: bytes) -> str:
    return hmac.new(WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest()


@pytest.fixture
def client():
    with patch("app.config.Settings.RAZORPAY_WEBHOOK_SECRET", WEBHOOK_SECRET):
        yield TestClient(app)


class TestRazorpayWebhook:
    def test_webhook_invalid_signature(self, client):
        payload = {"event": "payment.captured", "payload": {}}
        response = client.post(
            "/api/v1/webhooks/razorpay",
            json=payload,
            headers={"X-Razorpay-Signature": "invalid"},
        )
        assert response.status_code == 400

    def test_webhook_subscription_charged(self, client):
        payload = {
            "event": "subscription.charged",
            "payload": {
                "subscription": {
                    "entity": {
                        "id": "sub_test_123",
                        "notes": {"user_id": "550e8400-e29b-41d4-a716-446655440000"},
                    }
                }
            },
        }

        body = json.dumps(payload).encode()
        signature = sign_body(body)

        response = client.post(
            "/api/v1/webhooks/razorpay",
            json=payload,
            headers={"X-Razorpay-Signature": signature},
        )
        assert response.status_code == 200

    def test_webhook_payment_captured(self, client):
        payload = {
            "event": "payment.captured",
            "payload": {
                "payment": {
                    "entity": {
                        "id": "pay_test_123",
                        "notes": {
                            "user_id": "550e8400-e29b-41d4-a716-446655440000",
                            "pack_type": "booster_150",
                        },
                    }
                }
            },
        }

        body = json.dumps(payload).encode()
        signature = sign_body(body)

        with patch(
            "app.api.v1.webhooks.database.async_session.commit", new_callable=AsyncMock
        ):
            response = client.post(
                "/api/v1/webhooks/razorpay",
                json=payload,
                headers={"X-Razorpay-Signature": signature},
            )
            assert response.status_code == 200

    def test_webhook_subscription_cancelled(self, client):
        payload = {
            "event": "subscription.cancelled",
            "payload": {
                "subscription": {
                    "entity": {
                        "id": "sub_test_123",
                        "notes": {"user_id": "550e8400-e29b-41d4-a716-446655440000"},
                    }
                }
            },
        }

        body = json.dumps(payload).encode()
        signature = sign_body(body)

        response = client.post(
            "/api/v1/webhooks/razorpay",
            json=payload,
            headers={"X-Razorpay-Signature": signature},
        )
        assert response.status_code == 200
