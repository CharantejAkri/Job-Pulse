import asyncio
import time
import httpx
from typing import List
from datetime import datetime, timedelta
from sqlalchemy import select, update
from workers.celery_app import celery_app
from scraper.linkedin import scrape_linkedin
from scraper.naukri import scrape_naukri
from scraper.indeed import scrape_indeed
from scraper.enrichment import extract_hr_info, calculate_match_score, find_hr_email
from scraper.dedup import deduplicate_jobs


@celery_app.task(bind=True, max_retries=3)
def start_scrape_task(
    self,
    user_id: str,
    job_title: str,
    location: str,
    sources: List[str],
    date_posted: str = "past_24h",
):
    results = []

    source_map = {
        "linkedin": scrape_linkedin,
        "naukri": scrape_naukri,
        "indeed": scrape_indeed,
    }

    for source in sources:
        if source not in source_map:
            continue

        try:
            jobs = source_map[source](job_title, location, date_posted)
            results.extend(jobs)

            time.sleep(5)

        except Exception as e:
            self.retry(exc=e, countdown=60)

    deduplicated = deduplicate_jobs(results)

    enriched_jobs = []
    for job in deduplicated:
        hr_name = extract_hr_info(job.get("description", ""))
        hr_email = find_hr_email(job.get("company", ""), hr_name)
        match_score = calculate_match_score(user_id, job.get("description", ""))

        job["hr_name"] = hr_name
        job["hr_email"] = hr_email.get("email")
        job["hr_email_verified"] = hr_email.get("verified", False)
        job["match_score"] = match_score

        enriched_jobs.append(job)

        time.sleep(2)

    return {
        "status": "completed",
        "job_count": len(enriched_jobs),
        "jobs": enriched_jobs,
    }


@celery_app.task
def validate_job_links():
    from app.database import async_session
    from app.models import ScrapeJob
    import asyncio

    async def _validate():
        async with async_session() as db:
            cutoff = datetime.utcnow() - timedelta(hours=48)
            result = await db.execute(
                select(ScrapeJob)
                .where(
                    ScrapeJob.is_expired == False,
                    ScrapeJob.created_at <= cutoff,
                )
                .limit(200)
            )
            jobs = result.scalars().all()

            expired_count = 0
            for job in jobs:
                try:
                    resp = httpx.head(job.source_url, timeout=10, follow_redirects=True)
                    if resp.status_code >= 400:
                        job.is_expired = True
                        expired_count += 1
                except Exception:
                    job.is_expired = True
                    expired_count += 1

                time.sleep(0.5)

            await db.commit()
            return {"validated": len(jobs), "marked_expired": expired_count}

    return asyncio.run(_validate())
