## **Functional Requirements Document (FRD): JobPulse India**

## **1\. User Management & Authentication**

**Goal:** Secure the platform and manage user-specific data history.

- **FR-1.1: Registration:** The system shall allow users to register using Email/Password or **Google OAuth**.
- **FR-1.2: Profile Management:** Users shall be able to upload a **Resume (PDF/DOCX)**. The system must store this to facilitate AI Match Scoring.
- **FR-1.3: Session Management:** The system shall use **JWT (JSON Web Tokens)** to maintain secure login sessions across the dashboard and scraping modules.

## **2\. Subscription & Credit Engine**

**Goal:** Ensure the project remains profitable by controlling resource usage.

- **FR-2.1: Tier-Based Access:** The system shall restrict features (e.g., LinkedIn scraping, Excel export) based on the user's active **Razorpay Subscription tier**.
- **FR-2.2: Credit Deduction:** The system shall deduct **1 Credit** only upon a _successful_ scrape and HR enrichment. Failed scrapes shall not consume credits.
- **FR-2.3: Add-on Logic:** Subscription credits shall expire at the end of the billing cycle. **Add-on Credits** (purchased via top-ups) shall have no expiry and be consumed only after monthly credits reach zero.
- **FR-2.4: Payment Webhooks:** The system shall listen to **Razorpay Webhooks** to automatically update credit balances and subscription statuses in real-time.

## **3\. Scraping & Data Extraction**

**Goal:** Gather high-quality, structured job data from multiple sources.

- **FR-3.1: Source Selection:** Users shall be able to select specific sources (**LinkedIn, Naukri, Indeed**) via a checkbox interface before starting a search.
- **FR-3.2: Parameterized Input:** The system shall accept **Job Title, Location, and Date Posted** (e.g., "Past 24 hours") as search filters.
- **FR-3.3: Stealth Execution:** The system shall use **Playwright** with residential proxies to mimic human browsing behavior and bypass IP blocks.
- **FR-3.4: Data Parsing:** For every listing, the system shall extract: Title, Company, Description, Salary, and **HR/Poster Name**.

## **4\. AI Enrichment & Matching**

**Goal:** Add "Hidden" value to the data that standard job boards don't provide.

- **FR-4.1: HR Lead Discovery:** The system shall send extracted HR names to an enrichment API (e.g., **Hunter.io**) to find verified professional emails/phone numbers.
- **FR-4.2: AI Match Scoring:** The system shall use **OpenAI (GPT-4o-mini)** to compare the user's uploaded resume against the Job Description (JD) and generate a **Match Score (0-100%)**.
- **FR-4.3: Deduplication:** The system shall identify duplicate jobs across different websites and merge them into a single record to prevent redundant rows in the final export.

## **5\. History & Data Export**

**Goal:** Provide users with easy access to their previous work and downloads.

- **FR-5.1: Search Logs:** The system shall display a list of all **Previous Searches**. Clicking a log shall auto-fill the search parameters for a new run.
- **FR-5.2: Download Library:** The system shall store a history of generated files. Users shall be able to **re-download** any file from the past 30-365 days (depending on the tier).
- **FR-5.3: Export Engine:** The system shall use the **Pandas** library to convert the PostgreSQL data into a clean, formatted **.xlsx (Excel) or .csv** file for the user.

## **6\. Operational & Compliance Requirements**

- **FR-6.1: Rate Limiting:** The system shall implement a **5-10 second delay** between scraping requests to remain "polite" and comply with Indian IT Act ethical guidelines.
- **FR-6.2: Link Validation:** A background worker shall check "Saved" job links every 48 hours and mark them as **"Expired"** if the job is no longer available.
- **FR-6.3: GST Invoicing:** For every transaction, the system shall generate a **GST-compliant PDF invoice** via Razorpay and email it to the user.

## **Summary of Data Flow**

- **User logs in** and selects **LinkedIn + Naukri**.
- **User enters "React Developer"** and clicks **"Start Scrape"**.
- **Backend checks Credits** → If > 0, **Redis** triggers the **Playwright** scraper.
- **AI parses HR info** and calculates the **Match Score**.
- **Database saves the results** and adds the entry to the **User's History**.
- **User clicks "Export"** and receives the **Excel file.**
