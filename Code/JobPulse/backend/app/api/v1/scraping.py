from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.database import get_db
from app.api.v1.auth import get_current_user
from app.models import ScrapeJob, SearchLog
from app.schemas import (
    SearchRequest,
    SearchLogResponse,
    ScrapeJobResponse,
    ScrapeTaskResponse,
)
from workers.tasks import start_scrape_task

router = APIRouter()


@router.post("/start", response_model=ScrapeTaskResponse)
async def start_scrape(
    request: SearchRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not request.sources:
        raise HTTPException(
            status_code=400, detail="At least one source must be selected"
        )

    estimated_credits = len(request.sources) * 10

    task = start_scrape_task.delay(
        user_id=current_user["id"],
        job_title=request.job_title,
        location=request.location,
        sources=[s.value for s in request.sources],
        date_posted=request.date_posted,
    )

    return ScrapeTaskResponse(
        task_id=task.id,
        message="Scrape task queued successfully",
        estimated_credits=estimated_credits,
    )


@router.get("/tasks/{task_id}", response_model=dict)
async def get_task_status(
    task_id: str,
    current_user: dict = Depends(get_current_user),
):
    from workers.celery_app import celery_app

    result = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
    }


@router.get("/jobs", response_model=list[ScrapeJobResponse])
async def get_scraped_jobs(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ScrapeJob)
        .where(ScrapeJob.user_id == current_user["id"])
        .order_by(desc(ScrapeJob.created_at))
        .limit(100)
    )
    return result.scalars().all()


@router.get("/history", response_model=list[SearchLogResponse])
async def get_search_history(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(SearchLog)
        .where(SearchLog.user_id == current_user["id"])
        .order_by(desc(SearchLog.created_at))
        .limit(50)
    )
    return result.scalars().all()
