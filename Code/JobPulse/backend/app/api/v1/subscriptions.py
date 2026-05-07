from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.api.v1.auth import get_current_user
from app.models import Subscription, SubscriptionStatus
from app.schemas import SubscriptionResponse, CreditBalanceResponse
from app.config import get_settings, Settings
import razorpay

router = APIRouter()

PLAN_CONFIG = {
    "pro": {"razorpay_plan_id": None, "monthly_credits": 500, "price": 149900},
    "agency": {"razorpay_plan_id": None, "monthly_credits": 2500, "price": 499900},
}


@router.get("/status", response_model=SubscriptionResponse)
async def get_subscription_status(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Subscription)
        .where(
            Subscription.user_id == current_user["id"],
            Subscription.status == SubscriptionStatus.ACTIVE,
        )
        .order_by(Subscription.created_at.desc())
        .limit(1)
    )
    sub = result.scalar_one_or_none()
    if not sub:
        raise HTTPException(status_code=404, detail="No active subscription found")
    return sub


@router.post("/create", response_model=dict)
async def create_subscription(
    plan_type: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    if plan_type not in PLAN_CONFIG:
        raise HTTPException(status_code=400, detail="Invalid plan type")

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    subscription_data = {
        "plan_id": PLAN_CONFIG[plan_type]["razorpay_plan_id"],
        "customer_notify": 1,
        "quantity": 1,
        "total_count": 12,
        "start_at": None,
    }

    subscription = client.subscription.create(subscription_data)
    return {
        "subscription_id": subscription["id"],
        "short_url": subscription["short_url"],
    }


@router.get("/credits", response_model=CreditBalanceResponse)
async def get_credit_balance(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from app.models import CreditWallet, CreditType

    sub_result = await db.execute(
        select(CreditWallet).where(
            CreditWallet.user_id == current_user["id"],
            CreditWallet.credit_type == CreditType.SUBSCRIPTION,
        )
    )
    addon_result = await db.execute(
        select(CreditWallet).where(
            CreditWallet.user_id == current_user["id"],
            CreditWallet.credit_type == CreditType.ADDON,
        )
    )

    sub_wallet = sub_result.scalar_one_or_none()
    addon_wallet = addon_result.scalar_one_or_none()

    return CreditBalanceResponse(
        subscription_credits=sub_wallet.balance if sub_wallet else 0,
        addon_credits=addon_wallet.balance if addon_wallet else 0,
        total_credits=(sub_wallet.balance if sub_wallet else 0)
        + (addon_wallet.balance if addon_wallet else 0),
    )
