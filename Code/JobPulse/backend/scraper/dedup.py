from typing import List, Dict
import hashlib


def deduplicate_jobs(jobs: List[Dict]) -> List[Dict]:
    """
    Identifies duplicate jobs across different sources and merges them.
    Uses title + company + location hash to detect duplicates.
    """
    seen = {}
    unique_jobs = []

    for job in jobs:
        key = generate_job_key(job)

        if key in seen:
            existing = seen[key]
            existing["is_duplicate"] = True

            if not existing.get("hr_email") and job.get("hr_email"):
                existing["hr_email"] = job["hr_email"]
                existing["hr_name"] = job.get("hr_name")
                existing["hr_email_verified"] = job.get("hr_email_verified", False)

            if not existing.get("salary") and job.get("salary"):
                existing["salary"] = job["salary"]

            continue

        job["is_duplicate"] = False
        seen[key] = job
        unique_jobs.append(job)

    return unique_jobs


def generate_job_key(job: Dict) -> str:
    """
    Generates a unique hash for a job based on title, company, and location.
    """
    title = job.get("job_title", "").lower().strip()
    company = job.get("company", "").lower().strip()
    location = job.get("location", "").lower().strip()

    key_string = f"{title}|{company}|{location}"
    return hashlib.md5(key_string.encode()).hexdigest()
