from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://jobpulse:jobpulse_secret@localhost:5432/jobpulse"
    REDIS_URL: str = "redis://localhost:6379/0"

    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""

    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""
    RAZORPAY_WEBHOOK_SECRET: str = ""

    OPENAI_API_KEY: str = ""
    HUNTER_IO_API_KEY: str = ""
    BRIGHT_DATA_PROXY: str = ""

    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET: str = "change-this-in-production"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
