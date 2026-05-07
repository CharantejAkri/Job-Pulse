from fastapi import APIRouter
from app.api.v1 import auth, users, subscriptions, credits, scraping, exports, webhooks

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(
    subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"]
)
api_router.include_router(credits.router, prefix="/credits", tags=["Credits"])
api_router.include_router(scraping.router, prefix="/scraping", tags=["Scraping"])
api_router.include_router(exports.router, prefix="/exports", tags=["Exports"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
