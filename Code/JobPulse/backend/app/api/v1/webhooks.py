from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import RazorpayWebhookEvent
from app.config import get_settings, Settings
import razorpay
import hmac
import hashlib
import json

router = APIRouter()


@router.post("/razorpay")
async def razorpay_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature")

    expected_signature = hmac.new(
        settings.RAZORPAY_WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256,
    ).hexdigest()

    if signature != expected_signature:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    payload = json.loads(body)
    event = payload.get("event", "")

    if event == "subscription.charged":
        await handle_subscription_charged(payload, db)
    elif event == "payment.captured":
        await handle_payment_captured(payload, db)
    elif event == "subscription.cancelled":
        await handle_subscription_cancelled(payload, db)

    return {"status": "ok"}


async def handle_subscription_charged(payload: dict, db: AsyncSession):
    subscription = payload.get("payload", {}).get("subscription", {}).get("entity", {})
    user_id = subscription.get("notes", {}).get("user_id")
    if not user_id:
        return

    from app.models import CreditWallet, CreditType
    from sqlalchemy import select

    wallet = await db.execute(
        select(CreditWallet).where(
            CreditWallet.user_id == user_id,
            CreditWallet.credit_type == CreditType.SUBSCRIPTION,
        )
    )
    wallet = wallet.scalar_one_or_none()

    if wallet:
        wallet.balance += 500
        await db.commit()


async def handle_payment_captured(payload: dict, db: AsyncSession):
    payment = payload.get("payload", {}).get("payment", {}).get("entity", {})
    user_id = payment.get("notes", {}).get("user_id")
    pack_type = payment.get("notes", {}).get("pack_type")

    if not user_id or not pack_type:
        return

    addon_credits = {"booster_150": 150, "bulk_500": 500}
    credits_to_add = addon_credits.get(pack_type, 0)

    if credits_to_add:
        from app.models import CreditWallet, CreditType
        from sqlalchemy import select

        wallet = await db.execute(
            select(CreditWallet).where(
                CreditWallet.user_id == user_id,
                CreditWallet.credit_type == CreditType.ADDON,
            )
        )
        wallet = wallet.scalar_one_or_none()

        if wallet:
            wallet.balance += credits_to_add
        else:
            new_wallet = CreditWallet(
                user_id=user_id,
                credit_type=CreditType.ADDON,
                balance=credits_to_add,
            )
            db.add(new_wallet)

        await db.commit()


async def handle_subscription_cancelled(payload: dict, db: AsyncSession):
    subscription = payload.get("payload", {}).get("subscription", {}).get("entity", {})
    user_id = subscription.get("notes", {}).get("user_id")

    if not user_id:
        return

    from app.models import Subscription, SubscriptionStatus
    from sqlalchemy import select

    sub = await db.execute(
        select(Subscription).where(
            Subscription.user_id == user_id,
            Subscription.razorpay_subscription_id == subscription.get("id"),
        )
    )
    sub = sub.scalar_one_or_none()

    if sub:
        sub.status = SubscriptionStatus.CANCELLED
        await db.commit()
