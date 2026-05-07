"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-05-07

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("email", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("full_name", sa.String(255), nullable=True),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("role", sa.String(20), server_default="free"),
        sa.Column("resume_url", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "subscriptions",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column(
            "razorpay_subscription_id", sa.String(100), unique=True, nullable=True
        ),
        sa.Column("razorpay_plan_id", sa.String(100), nullable=True),
        sa.Column("status", sa.String(20), server_default="active"),
        sa.Column("plan_type", sa.String(20), nullable=False),
        sa.Column("monthly_credits", sa.Integer, server_default="0"),
        sa.Column("current_period_start", sa.DateTime, nullable=True),
        sa.Column("current_period_end", sa.DateTime, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "credit_wallets",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column("credit_type", sa.String(20), server_default="subscription"),
        sa.Column("balance", sa.Integer, server_default="0"),
        sa.Column("expires_at", sa.DateTime, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "credit_transactions",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column(
            "wallet_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("credit_wallets.id"),
            nullable=True,
        ),
        sa.Column("amount", sa.Integer, nullable=False),
        sa.Column("type", sa.String(20), nullable=False),
        sa.Column("description", sa.String(255), nullable=True),
        sa.Column("razorpay_payment_id", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "search_logs",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column("job_title", sa.String(255), nullable=False),
        sa.Column("location", sa.String(255), nullable=True),
        sa.Column("sources", postgresql.JSONB, nullable=False),
        sa.Column("date_posted", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "scrape_jobs",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column(
            "search_log_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("search_logs.id"),
            nullable=True,
        ),
        sa.Column("job_title", sa.String(255), nullable=False),
        sa.Column("company", sa.String(255), nullable=False),
        sa.Column("location", sa.String(255), nullable=True),
        sa.Column("salary", sa.String(100), nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("source", sa.String(20), nullable=False),
        sa.Column("source_url", sa.String(1000), nullable=False),
        sa.Column("hr_name", sa.String(255), nullable=True),
        sa.Column("hr_email", sa.String(255), nullable=True),
        sa.Column("hr_email_verified", sa.Boolean, server_default="false"),
        sa.Column("match_score", sa.Float, nullable=True),
        sa.Column("status", sa.String(20), server_default="pending"),
        sa.Column("is_expired", sa.Boolean, server_default="false"),
        sa.Column("is_duplicate", sa.Boolean, server_default="false"),
        sa.Column("scraped_at", sa.DateTime, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_index("ix_scrape_jobs_user_id", "scrape_jobs", ["user_id"])
    op.create_index("ix_scrape_jobs_location", "scrape_jobs", ["location"])
    op.create_index("ix_scrape_jobs_job_title", "scrape_jobs", ["job_title"])

    op.create_table(
        "download_history",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column("file_name", sa.String(255), nullable=False),
        sa.Column("file_path", sa.String(500), nullable=False),
        sa.Column("file_format", sa.String(10), nullable=False),
        sa.Column("job_count", sa.Integer, server_default="0"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("expires_at", sa.DateTime, nullable=True),
    )


def downgrade() -> None:
    op.drop_table("download_history")
    op.drop_table("scrape_jobs")
    op.drop_table("search_logs")
    op.drop_table("credit_transactions")
    op.drop_table("credit_wallets")
    op.drop_table("subscriptions")
    op.drop_table("users")
