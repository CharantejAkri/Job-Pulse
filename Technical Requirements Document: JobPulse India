## **Technical Requirements Document: JobPulse**

## **1\. System Architecture Overview**

The system follows a **decoupled micro-services architecture** to ensure that a slow scraping task doesn't crash the main website.

- **Frontend Layer:** Next.js (React) for a fast, SEO-friendly user interface.
- **API Layer:** Node.js (Express) or Python (FastAPI) to handle user requests and history.
- **Task Queue:** Redis + Celery to manage long-running scrapes in the background.
- **Data Layer:** PostgreSQL for structured user and job data storage.

## **2\. Core Technical Components & "The Why"**

## **A. Scraping Engine: Playwright (vs. Selenium)**

- **Why Playwright?** Playwright is modern and faster because it uses **WebSockets** to talk directly to the browser, unlike Selenium which uses the slower HTTP-based WebDriver protocol.
- **Key Feature:** **Auto-waiting.** Playwright automatically waits for job cards to load before trying to scrape them, which prevents the common "Element not found" errors seen in older tools.

## **B. Background Tasks: Redis + Celery**

- **Why use them?** Scraping 500 jobs takes minutes. If you run this in the main API, the user's screen will freeze.
- **The Workflow:** When a user clicks "Scrape," the API sends a "task" to **Redis** (the message broker). A **Celery Worker** picks up the task and scrapes in the background while the user continues to browse their history.

## **C. Database: PostgreSQL**

- **Why not MongoDB?** Job data is highly structured (Job ID, Title, Salary). PostgreSQL's **Relational Schema** allows for faster filtering (e.g., "Show me all Mumbai jobs with > ₹15L salary") and ensures data integrity through strict foreign keys.

## **D. Intelligence: GPT-4o-mini-API**

- **Why AI?** Every website formats its job description differently. Instead of writing 100 different "regex" rules, we send the text to GPT-4o-mini to **instantly extract** the Recruiter's Name and Match Score. It is significantly cheaper than human data entry or complex custom NLP models.

## **3\. Data Flow & Security**

- **Identity:** Authentication is handled via **Supabase Auth (JWT)**. No user can access another user's "Scrape History".
- **Enrichment Pipeline:** Raw job data → AI Parsing → Hunter.io (Email Verification) → PostgreSQL.
- **Payment Security:** The system uses **Razorpay Webhooks**. Credits are only added after the Razorpay server confirms the transaction is "Captured".

## **4\. Technical Constraints & Risks**

| **Risk**           | **Technical Solution**                                                                                                                                                                                                  |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **IP Banning**     | **Bright Data Proxies**: Rotates IP addresses every few requests so [LinkedIn](https://www.linkedin.com/pulse/belitsoft-explains-why-playwright-better-than-selenium-2025-m7u7e) thinks multiple "humans" are visiting. |
| **Data Staleness** | **Cron Jobs**: A scheduled task runs every 48 hours to "ping" job links. If they are dead, they are marked as inactive in the DB.                                                                                       |
| **Database Bloat** | **Indexing**: All city and job_title columns will be indexed to keep search speeds under 100ms as the DB grows.                                                                                                         |

## **Summary: The "Why" behind the Stack**

We chose **Playwright** for speed, **Redis** for non-blocking performance, **PostgreSQL** for data accuracy, and **Razorpay** for Indian payment compliance. This combination ensures the app can handle 1,000+ concurrent users without slowing down.
