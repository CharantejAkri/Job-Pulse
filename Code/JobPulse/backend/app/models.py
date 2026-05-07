import enum
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    Enum as SAEnum,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from app.database import Base


class UserRole(str, enum.Enum):
    FREE = "free"
    PRO = "pro"
    AGENCY = "agency"


class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    PAST_DUE = "past_due"


class CreditType(str, enum.Enum):
    SUBSCRIPTION = "subscription"
    ADDON = "addon"


class JobSource(str, enum.Enum):
    LINKEDIN = "linkedin"
    NUKRI = "naukri"
    INDEED = "indeed"


class ScrapeStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    role = Column(SAEnum(UserRole), default=UserRole.FREE)
    resume_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subscriptions = relationship("Subscription", back_populates="user")
    credit_wallets = relationship("CreditWallet", back_populates="user")
    search_logs = relationship("SearchLog", back_populates="user")
    scrape_jobs = relationship("ScrapeJob", back_populates="user")
    download_history = relationship("DownloadHistory", back_populates="user")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    razorpay_subscription_id = Column(String(100), unique=True, nullable=True)
    razorpay_plan_id = Column(String(100), nullable=True)
    status = Column(SAEnum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)
    plan_type = Column(SAEnum(UserRole), nullable=False)
    monthly_credits = Column(Integer, default=0)
    current_period_start = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="subscriptions")


class CreditWallet(Base):
    __tablename__ = "credit_wallets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    credit_type = Column(SAEnum(CreditType), default=CreditType.SUBSCRIPTION)
    balance = Column(Integer, default=0)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="credit_wallets")


class CreditTransaction(Base):
    __tablename__ = "credit_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    wallet_id = Column(
        UUID(as_uuid=True), ForeignKey("credit_wallets.id"), nullable=True
    )
    amount = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False)
    description = Column(String(255), nullable=True)
    razorpay_payment_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class SearchLog(Base):
    __tablename__ = "search_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    job_title = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)
    sources = Column(JSONB, nullable=False)
    date_posted = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="search_logs")


class ScrapeJob(Base):
    __tablename__ = "scrape_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    search_log_id = Column(
        UUID(as_uuid=True), ForeignKey("search_logs.id"), nullable=True
    )
    job_title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)
    salary = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    source = Column(SAEnum(JobSource), nullable=False)
    source_url = Column(String(1000), nullable=False)
    hr_name = Column(String(255), nullable=True)
    hr_email = Column(String(255), nullable=True)
    hr_email_verified = Column(Boolean, default=False)
    match_score = Column(Float, nullable=True)
    status = Column(SAEnum(ScrapeStatus), default=ScrapeStatus.PENDING)
    is_expired = Column(Boolean, default=False)
    is_duplicate = Column(Boolean, default=False)
    scraped_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="scrape_jobs")


class DownloadHistory(Base):
    __tablename__ = "download_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_format = Column(String(10), nullable=False)
    job_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="download_history")
