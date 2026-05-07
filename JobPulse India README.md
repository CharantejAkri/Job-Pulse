## **Project Master Specification: JobPulse India**

**"A high-margin, India-compliant job lead generation and recruitment tool."**

## **1\. Project Concept**

**JobPulse** is a professional intelligence engine that allows registered Indian users to select specific local and global job boards (LinkedIn, Naukri, Indeed), extract detailed job leads-including HR contact information-and export them into structured formats for offline networking and applications.

## **2\. User Lifecycle & India-Specific Registration**

To maintain high trust and data residency, the application follows a secure, authenticated lifecycle:

- **Registration**: Users register via Email or Social Login (Google). OTP-based verification for Indian mobile numbers can be added to reduce bot accounts.
- **Resume Profile**: Users upload their resume in .pdf format to trigger the **AI Match %** feature.
- **Dashboard & History**:
  - **Search Logs**: All past searches (e.g., "SDE-2 in Mumbai") are saved for one-click re-runs.
  - **Download History**: Access to every Excel/CSV file previously exported.

## **3\. The Indian Monetization Model (Profit-Focused)**

The app uses a **Multi-Tiered Subscription** model designed for the Indian market, ensuring you cover your [API costs](https://razorpay.com/learn/payment-solutions-subscriptions-saas-india/) while maintaining profit.

| **Plan**       | **Price (INR)** | **Credits/Month** | **Profit Goal** | **Key Features**                               |
| -------------- | --------------- | ----------------- | --------------- | ---------------------------------------------- |
| **Freemium**   | ₹0              | 5                 | -               | Basic search, Indeed only, no HR leads.        |
| **Pro Hunter** | **₹1,499**      | **500**           | **₹600+**       | All sites, HR Contact Info, AI Match %, Excel. |
| **Agency**     | **₹4,999**      | **2,500**         | **₹2,500+**     | Team access, Priority scraping, API export.    |

## **High-Margin Add-Ons (Top-Ups)**

Users can buy extra credits if they run out mid-month. Add-on credits **never expire**.

- **Booster Pack**: ₹599 for 150 Credits.
- **Bulk Refill**: ₹1,299 for 500 Credits.

## **4\. Technical Architecture (India-First Stack)**

Using local regions and Indian payment gateways ensures low latency and high transaction success rates.

| **Layer**           | **Tool / Provider**                                 | **Why this choice?**                                                                                                                  |
| ------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Identity**        | [Supabase Auth](https://supabase.com/auth)          | Open-source, handles JWT and user history natively.                                                                                   |
| **Payments**        | Razorpay Subscriptions                              | Native support for **UPI AutoPay**, cards, and GST-compliant invoicing.                                                               |
| **Hosting**         | AWS Mumbai Region                                   | Ensures sub-30ms latency and complies with [Indian data residency laws](https://utho.com/blog/top-cloud-service-providers-in-india/). |
| **Scraper**         | Playwright + [Bright Data](https://brightdata.com/) | Best-in-class stealth to avoid being blocked by LinkedIn/Naukri.                                                                      |
| **AI Intelligence** | [OpenAI GPT-4o-mini](https://openai.com/api/)       | Cheap and fast extraction of HR names from messy descriptions.                                                                        |
| **Leads**           | [Hunter.io](https://hunter.io/)                     | Industry standard for finding verified professional emails.                                                                           |

## **5\. Functional Requirements for Billing**

- **GST-Ready Invoicing**: Every payment must trigger a GST-compliant invoice sent automatically to the user's email via [Razorpay Invoices](https://razorpay.com/invoices/).
- **Credit Drawdown**: Subscriptions credits are used first; Add-on credits are used only when the monthly balance is ₹0.
- **Webhook Integration**: The backend must listen to [Razorpay webhooks](https://razorpay.com/docs/payments/subscriptions/integration-guide/) to automatically update user_credits upon successful payment.

## **6\. Compliance & Legal Guardrails (India 2024-2025)**

- [**DPDP Act 2023**](https://go4scrap.in/kb/legal-ethics/scraping-in-india-2025/) **Compliance**: Focus on "Publicly Available Data." Do not scrape behind login gates to stay within legal boundaries.
- **Polite Crawling**: Implement a 5-10 second delay between requests to avoid being flagged as a cyber-attack under [Section 43 of the IT Act](https://spiceroutelegal.com/publications/legality-of-data-scraping-under-indian-law/).
- **Data Audit**: Retain transaction and user logs for 10 years as per [Razorpay T&C and Govt. guidelines](https://razorpay.com/terms/).

## **7\. Sample Export Data (Final Excel File)**

The downloadable file will be organized as follows:

**Job Title** | **Company** | **Location** | **Salary** | **HR Name** | **HR Verified Email** | **Match Score %** | **Original URL** | **Scrape Date**
