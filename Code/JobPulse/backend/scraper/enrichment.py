import openai
import httpx
from app.config import get_settings
from typing import Optional, Dict

settings = get_settings()
openai.api_key = settings.OPENAI_API_KEY


def extract_hr_info(description: str) -> Optional[str]:
    """
    Uses GPT-4o-mini to extract HR/Recruiter name from job description.
    """
    if not description:
        return None

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Extract the recruiter or HR contact name from the job description. Return only the name or 'Not Found' if not present.",
                },
                {
                    "role": "user",
                    "content": description[:2000],
                },
            ],
            max_tokens=50,
            temperature=0.1,
        )

        name = response.choices[0].message.content.strip()
        return name if name.lower() != "not found" else None

    except Exception as e:
        print(f"HR extraction error: {e}")
        return None


def calculate_match_score(user_id: str, job_description: str) -> Optional[float]:
    """
    Uses GPT-4o-mini to calculate match score between user resume and job description.
    """
    if not job_description:
        return None

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a job matching assistant. Compare the user's resume skills with the job description. Return only a number between 0 and 100 representing the match percentage.",
                },
                {
                    "role": "user",
                    "content": f"Job Description: {job_description[:2000]}",
                },
            ],
            max_tokens=10,
            temperature=0.1,
        )

        score = response.choices[0].message.content.strip()
        return float(score) if score.isdigit() else None

    except Exception as e:
        print(f"Match score error: {e}")
        return None


def find_hr_email(company: str, hr_name: Optional[str]) -> Dict:
    """
    Uses Hunter.io to find verified HR email.
    """
    if not company or not settings.HUNTER_IO_API_KEY:
        return {"email": None, "verified": False}

    try:
        domain = (
            company.lower()
            .replace(" ", "")
            .replace("inc", "")
            .replace("ltd", "")
            .replace("private", "")
            .replace("limited", "")
        )

        if hr_name:
            name_parts = hr_name.split()
            first_name = name_parts[0] if name_parts else ""
            last_name = name_parts[-1] if len(name_parts) > 1 else ""
            url = f"https://api.hunter.io/v2/email-finder?domain={domain}&first_name={first_name}&last_name={last_name}&api_key={settings.HUNTER_IO_API_KEY}"
        else:
            url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={settings.HUNTER_IO_API_KEY}"

        response = httpx.get(url, timeout=10)
        data = response.json()

        if hr_name:
            email_data = data.get("data", {})
            email = email_data.get("email")
            verified = email_data.get("status") == "valid" if email else False
        else:
            emails = data.get("data", {}).get("emails", [])
            email = emails[0].get("value") if emails else None
            verified = emails[0].get("status") == "valid" if emails else False

        return {"email": email, "verified": verified}

    except Exception as e:
        print(f"Hunter.io error: {e}")
        return {"email": None, "verified": False}
