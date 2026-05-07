Free-Tier App building

## **1\. The "Zero-Money" Tech Stack**

| **Component**       | **Tool**                     | **Why it's Free**                                                                 |
| ------------------- | ---------------------------- | --------------------------------------------------------------------------------- |
| **Frontend UI**     | **Next.js + Vercel**         | Vercel's "Hobby" tier is free for personal projects \[1\].                        |
| **Database**        | **Supabase (PostgreSQL)**    | Free tier includes 500MB of storage-suitable for many jobs.                       |
| **Auth**            | **Supabase Auth**            | Free for up to 50,000 monthly users.                                              |
| **Scraper**         | **Playwright (Python/Node)** | Open-source. Running it on a personal laptop utilizes personal resources.         |
| **AI Intelligence** | **Gemini 1.5 Flash**         | Google AI Studio provides a **free API** (limited requests per minute).           |
| **Data Enrichment** | **Manual/OSINT**             | Instead of paid APIs, just scrape the "Poster Name" and search LinkedIn manually. |

## **2\. How the "Zero-Cost" Workflow Works**

Free hosting services, such as Vercel, do not support long-running scraping scripts, therefore, the scraper will be run **locally**.

- **Local Scraper**: A script runs on a personal laptop. It opens a browser, scrapes LinkedIn/Naukri, and extracts the data.
- **API Upload**: The script sends data directly to **Supabase** using an API key.
- **Cloud Dashboard**: A project.vercel.app website is accessed. It fetches the data from Supabase and displays it in the UI.
- **Local Export**: The local script can generate the Excel file directly, or the website can use a library like xlsx to do it in the browser for free.

## **3\. Smart "Hacks" to Avoid Costs**

- **Avoid Proxies**: Since the scraping is for personal use, there is no need to hide. Add a **random delay** (e.g., time.sleep(random.uniform(5, 10))) between pages so the websites do not block the personal internet connection.
- **The Gemini Hack**: Use the **Gemini 1.5 Flash API**. It's faster and has a higher free limit than GPT-4. Send it the raw job text and ask: _"Extract: Job Title, HR Name, and Salary from this text."_
- **No Paid HR Leads**: Instead of paying Hunter.io, just extract the **HR's LinkedIn Profile URL**. In the dashboard, make it a clickable button: **"Message HR"**.

## **4\. Updated Technical Architecture**

- **Database Schema**:
  - profiles: Stores user info.
  - jobs: Stores title, company, jd, hr_name, source_url, and match_score.
  - searches: Stores history of search terms.
- **The Scraper**: Use **Playwright**. It's easier to debug than Selenium. It can run in "headed" mode (where the browser opens) to solve any CAPTCHAs manually for free.

## **5\. Why This Is a Good "Personal Project"**

This is a **top-tier portfolio piece**. Employers value:

- **Efficiency**: Gemini Flash is used to save costs.
- **System Design**: A local script is connected to a cloud database.
- **Utility**: The project helps with job searching.
