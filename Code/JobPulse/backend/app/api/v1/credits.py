from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, desc
from app.database import get_db
from app.api.v1.auth import get_current_user
from app.models import CreditWallet, CreditTransaction, CreditType
from app.schemas import (
    CreditBalanceResponse,
    CreditTopUpRequest,
    CreditTransactionResponse,
)
from app.config import get_settings, Settings
import razorpay

router = APIRouter()

ADDON_CONFIG = {
    "booster_150": {"credits": 150, "price": 59900},
    "bulk_500": {"credits": 500, "price": 129900},
}


@router.get("/balance", response_model=CreditBalanceResponse)
async def get_balance(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    sub_wallet = await db.execute(
        select(CreditWallet).where(
            CreditWallet.user_id == current_user["id"],
            CreditWallet.credit_type == CreditType.SUBSCRIPTION,
        )
    )
    addon_wallet = await db.execute(
        select(CreditWallet).where(
            CreditWallet.user_id == current_user["id"],
            CreditWallet.credit_type == CreditType.ADDON,
        )
    )

    sub_balance = sub_wallet.scalar_one_or_none()
    addon_balance = addon_wallet.scalar_one_or_none()

    return CreditBalanceResponse(
        subscription_credits=sub_balance.balance if sub_balance else 0,
        addon_credits=addon_balance.balance if addon_balance else 0,
        total_credits=(sub_balance.balance if sub_balance else 0)
        + (addon_balance.balance if addon_balance else 0),
    )


@router.post("/topup", response_model=dict)
async def create_topup_order(
    request: CreditTopUpRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    if request.pack_type not in ADDON_CONFIG:
        raise HTTPException(status_code=400, detail="Invalid pack type")

    pack = ADDON_CONFIG[request.pack_type]

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    order = client.order.create(
        {
            "amount": pack["price"],
            "currency": "INR",
            "receipt": f"topup_{current_user['id']}_{request.pack_type}",
            "payment_capture": 1,
        }
    )

    return {
        "order_id": order["id"],
        "amount": pack["price"],
        "currency": "INR",
        "credits": pack["credits"],
    }


@router.get("/transactions", response_model=list[CreditTransactionResponse])
async def get_transactions(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(CreditTransaction)
        .where(CreditTransaction.user_id == current_user["id"])
        .order_by(desc(CreditTransaction.created_at))
        .limit(50)
    )
    return result.scalars().all()
