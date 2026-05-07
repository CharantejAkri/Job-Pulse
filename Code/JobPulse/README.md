# JobPulse India

India's premier job lead generation and recruitment tool. Extract verified job leads with HR contacts from LinkedIn, Naukri, and Indeed with AI-powered match scoring.

## Architecture

```
JobPulse/
├── frontend/          # Next.js 14 + React + Tailwind CSS
├── backend/           # FastAPI (Python) + SQLAlchemy
│   ├── app/           # API routes, models, schemas
│   ├── scraper/       # Playwright scrapers (LinkedIn, Naukri, Indeed)
│   ├── workers/       # Celery background tasks
│   └── alembic/       # Database migrations
├── docker-compose.yml # Local development stack
└── README.md
```

## Tech Stack

| Layer           | Technology                          |
| --------------- | ----------------------------------- |
| Frontend        | Next.js 14, React, Tailwind CSS     |
| Backend API     | FastAPI, SQLAlchemy, AsyncPG        |
| Auth            | Supabase Auth (JWT + Google OAuth)  |
| Database        | PostgreSQL 15                       |
| Task Queue      | Redis + Celery                      |
| Scraping        | Playwright + Bright Data Proxies    |
| AI              | OpenAI GPT-4o-mini                  |
| Email Discovery | Hunter.io                           |
| Payments        | Razorpay Subscriptions (UPI AutoPay)|
| Hosting         | AWS Mumbai Region                   |

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for local frontend dev)
- Python 3.11+ (for local backend dev)

### 1. Clone & Configure

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
```

Edit `.env` files with your API keys:
- Supabase project URL & keys
- Razorpay test keys
- OpenAI API key
- Hunter.io API key
- Bright Data proxy credentials

### 2. Start with Docker

```bash
docker-compose up -d
```

This starts:
- PostgreSQL on port 5432
- Redis on port 6379
- FastAPI backend on port 8000
- Celery worker & beat scheduler
- Next.js frontend on port 3000

### 3. Run Database Migrations

```bash
docker exec jobpulse-api alembic upgrade head
```

### 4. Access the App

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs (Swagger UI)
- Health Check: http://localhost:8000/health

## Local Development (without Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
playwright install chromium
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

| Method | Path                              | Description                |
| ------ | --------------------------------- | -------------------------- |
| GET    | `/api/v1/auth/me`                 | Get current user profile   |
| POST   | `/api/v1/users/resume`            | Upload resume              |
| GET    | `/api/v1/credits/balance`         | Check credit balance       |
| POST   | `/api/v1/credits/topup`           | Purchase credit add-on     |
| POST   | `/api/v1/scraping/start`          | Start a new scrape task    |
| GET    | `/api/v1/scraping/tasks/{id}`     | Check task status          |
| GET    | `/api/v1/scraping/jobs`           | Get scraped jobs           |
| GET    | `/api/v1/scraping/history`        | Get search history         |
| POST   | `/api/v1/exports/generate`        | Generate Excel/CSV export  |
| GET    | `/api/v1/exports/download/{file}` | Download exported file     |
| POST   | `/api/v1/webhooks/razorpay`       | Razorpay webhook handler   |

## Subscription Plans

| Plan       | Price    | Credits | Features                              |
| ---------- | -------- | ------- | ------------------------------------- |
| Freemium   | ₹0       | 5       | Basic search, Indeed only             |
| Pro Hunter | ₹1,499   | 500     | All sites, HR contacts, AI Match, Excel |
| Agency     | ₹4,999   | 2,500   | Team access, Priority scraping, API   |

### Add-on Credits

- **Booster Pack**: ₹599 for 150 credits (never expire)
- **Bulk Refill**: ₹1,299 for 500 credits (never expire)

## Compliance

- **DPDP Act 2023**: Only scrapes publicly available data
- **IT Act Section 43**: 5-10 second delay between requests
- **GST Invoicing**: Auto-generated via Razorpay for every transaction
- **Data Retention**: 10-year retention for transaction logs

## License

Proprietary - JobPulse India 2026
