from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.models import UserRole, SubscriptionStatus, CreditType, JobSource, ScrapeStatus


class UserCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: Optional[str]
    role: UserRole
    resume_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ResumeUploadResponse(BaseModel):
    resume_url: str
    message: str


class SubscriptionCreate(BaseModel):
    plan_type: UserRole
    razorpay_subscription_id: Optional[str] = None
    razorpay_plan_id: Optional[str] = None


class SubscriptionResponse(BaseModel):
    id: UUID
    user_id: UUID
    status: SubscriptionStatus
    plan_type: UserRole
    monthly_credits: int
    current_period_end: Optional[datetime]

    class Config:
        from_attributes = True


class CreditBalanceResponse(BaseModel):
    subscription_credits: int
    addon_credits: int
    total_credits: int


class CreditTopUpRequest(BaseModel):
    pack_type: str = Field(..., description="booster_150 or bulk_500")
    razorpay_payment_id: str


class CreditTransactionResponse(BaseModel):
    id: UUID
    amount: int
    type: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class SearchRequest(BaseModel):
    job_title: str
    location: Optional[str] = None
    sources: List[JobSource]
    date_posted: Optional[str] = "past_24h"


class SearchLogResponse(BaseModel):
    id: UUID
    job_title: str
    location: Optional[str]
    sources: List[str]
    date_posted: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ScrapeJobResponse(BaseModel):
    id: UUID
    job_title: str
    company: str
    location: Optional[str]
    salary: Optional[str]
    source: JobSource
    source_url: str
    hr_name: Optional[str]
    hr_email: Optional[str]
    hr_email_verified: bool
    match_score: Optional[float]
    status: ScrapeStatus
    scraped_at: Optional[datetime]

    class Config:
        from_attributes = True


class ScrapeTaskResponse(BaseModel):
    task_id: str
    message: str
    estimated_credits: int


class DownloadHistoryResponse(BaseModel):
    id: UUID
    file_name: str
    file_format: str
    job_count: int
    created_at: datetime
    expires_at: Optional[datetime]

    class Config:
        from_attributes = True


class RazorpayWebhookEvent(BaseModel):
    event: str
    payload: dict
