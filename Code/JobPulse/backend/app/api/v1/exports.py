from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.database import get_db
from app.api.v1.auth import get_current_user
from app.models import ScrapeJob, DownloadHistory
from app.schemas import DownloadHistoryResponse
import pandas as pd
import os
from datetime import datetime
from uuid import uuid4

router = APIRouter()

EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)


@router.post("/generate", response_model=dict)
async def generate_export(
    file_format: str = "xlsx",
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if file_format not in ["xlsx", "csv"]:
        raise HTTPException(status_code=400, detail="Format must be xlsx or csv")

    result = await db.execute(
        select(ScrapeJob)
        .where(
            ScrapeJob.user_id == current_user["id"],
            ScrapeJob.status == "completed",
            ScrapeJob.is_duplicate == False,
        )
        .order_by(desc(ScrapeJob.scraped_at))
    )
    jobs = result.scalars().all()

    rows = []
    for job in jobs:
        rows.append(
            {
                "Job Title": job.job_title,
                "Company": job.company,
                "Location": job.location or "",
                "Salary": job.salary or "",
                "HR Name": job.hr_name or "",
                "HR Verified Email": job.hr_email or "",
                "Match Score %": job.match_score if job.match_score else "",
                "Original URL": job.source_url,
                "Scrape Date": job.scraped_at.strftime("%Y-%m-%d %H:%M")
                if job.scraped_at
                else "",
            }
        )

    filename = f"jobpulse_{current_user['id']}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{file_format}"
    filepath = os.path.join(EXPORT_DIR, filename)

    df = (
        pd.DataFrame(rows)
        if rows
        else pd.DataFrame(
            columns=[
                "Job Title",
                "Company",
                "Location",
                "Salary",
                "HR Name",
                "HR Verified Email",
                "Match Score %",
                "Original URL",
                "Scrape Date",
            ]
        )
    )

    if file_format == "xlsx":
        df.to_excel(filepath, index=False)
    else:
        df.to_csv(filepath, index=False)

    return {
        "file_id": str(uuid4()),
        "file_name": filename,
        "job_count": len(jobs),
        "download_url": f"/api/v1/exports/download/{filename}",
    }


@router.get("/download/{filename}")
async def download_file(
    filename: str,
    current_user: dict = Depends(get_current_user),
):
    filepath = os.path.join(EXPORT_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(filepath, filename=filename)


@router.get("/history", response_model=list[DownloadHistoryResponse])
async def get_download_history(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(DownloadHistory)
        .where(DownloadHistory.user_id == current_user["id"])
        .order_by(desc(DownloadHistory.created_at))
        .limit(50)
    )
    return result.scalars().all()
