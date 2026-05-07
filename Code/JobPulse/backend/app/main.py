import asyncio
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from app.config import get_settings
from app.database import engine, Base, async_session
from app.api.v1.router import api_router
import redis.asyncio as redis

settings = get_settings()

app = FastAPI(
    title="JobPulse API",
    description="India's premier job lead generation and recruitment tool",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://jobpulse.in"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/health/detail")
async def health_detail():
    checks = {}

    try:
        async with async_session() as session:
            await session.execute(text("SELECT 1"))
            checks["database"] = {"status": "connected", "type": "postgresql"}
    except Exception as e:
        checks["database"] = {"status": "error", "detail": str(e)}

    try:
        r = redis.from_url(settings.REDIS_URL, socket_connect_timeout=3)
        await r.ping()
        await r.aclose()
        checks["redis"] = {"status": "connected"}
    except Exception as e:
        checks["redis"] = {"status": "error", "detail": str(e)}

    all_healthy = all(check.get("status") == "connected" for check in checks.values())

    status_code = 200 if all_healthy else 503

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "healthy" if all_healthy else "degraded",
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat(),
            "uptime_seconds": (datetime.utcnow() - app.state.start_time).seconds
            if hasattr(app.state, "start_time")
            else 0,
            "checks": checks,
        },
    )


@app.on_event("startup")
async def set_start_time():
    app.state.start_time = datetime.utcnow()
