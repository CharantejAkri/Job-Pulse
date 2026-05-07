import pytest
from scraper.dedup import deduplicate_jobs, generate_job_key


class TestDedup:
    def test_no_duplicates(self):
        jobs = [
            {
                "job_title": "React Developer",
                "company": "Google",
                "location": "Bangalore",
            },
            {
                "job_title": "Backend Developer",
                "company": "Flipkart",
                "location": "Mumbai",
            },
        ]
        result = deduplicate_jobs(jobs)
        assert len(result) == 2
        assert all(j["is_duplicate"] == False for j in result)

    def test_exact_duplicate_merged(self):
        jobs = [
            {
                "job_title": "React Developer",
                "company": "Google",
                "location": "Bangalore",
                "salary": "₹20L",
                "hr_email": "",
            },
            {
                "job_title": "React Developer",
                "company": "Google",
                "location": "Bangalore",
                "salary": "",
                "hr_email": "hr@google.com",
            },
        ]
        result = deduplicate_jobs(jobs)
        assert len(result) == 1
        assert result[0]["hr_email"] == "hr@google.com"
        assert result[0]["salary"] == "₹20L"

    def test_case_insensitive_dedup(self):
        jobs = [
            {
                "job_title": "React Developer",
                "company": "Google",
                "location": "Bangalore",
            },
            {
                "job_title": "react developer",
                "company": "google",
                "location": "bangalore",
            },
        ]
        result = deduplicate_jobs(jobs)
        assert len(result) == 1

    def test_different_jobs_same_company(self):
        jobs = [
            {
                "job_title": "Frontend Developer",
                "company": "Google",
                "location": "Bangalore",
            },
            {
                "job_title": "Backend Developer",
                "company": "Google",
                "location": "Bangalore",
            },
        ]
        result = deduplicate_jobs(jobs)
        assert len(result) == 2


class TestGenerateJobKey:
    def test_key_consistency(self):
        job1 = {
            "job_title": "  React Developer  ",
            "company": "  Google  ",
            "location": "  Bangalore  ",
        }
        job2 = {
            "job_title": "react developer",
            "company": "google",
            "location": "bangalore",
        }
        assert generate_job_key(job1) == generate_job_key(job2)

    def test_key_uniqueness(self):
        job1 = {
            "job_title": "React Developer",
            "company": "Google",
            "location": "Bangalore",
        }
        job2 = {
            "job_title": "React Developer",
            "company": "Google",
            "location": "Mumbai",
        }
        assert generate_job_key(job1) != generate_job_key(job2)
