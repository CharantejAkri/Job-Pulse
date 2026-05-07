# JobPulse India - Setup Guide

This guide covers all installation methods. Choose the one that fits your environment.

## Prerequisites

| Tool           | Version | Required For          |
| -------------- | ------- | --------------------- |
| Python         | 3.11+   | Backend API, Scrapers |
| Node.js        | 18+     | Frontend              |
| PostgreSQL     | 15+     | Database              |
| Redis          | 7+      | Task Queue            |
| Docker         | 20+     | All-in-one setup      |

## Quick Install

### Windows
```powershell
.\setup.ps1
```

### Linux/Mac
```bash
chmod +x setup.sh && ./setup.sh
```

## Manual Installation

### 1. Python & Backend

```bash
# Install Python 3.11 from https://www.python.org/downloads/
# Make sure "Add to PATH" is checked during installation

# Create virtual environment
cd backend
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
playwright install-deps
```

### 2. Node.js & Frontend

```bash
# Install Node.js 18+ from https://nodejs.org/

cd frontend
npm install
```

### 3. PostgreSQL

**Option A: Docker (Recommended)**
```bash
docker run -d --name jobpulse-db -e POSTGRES_USER=jobpulse -e POSTGRES_PASSWORD=jobpulse_secret -e POSTGRES_DB=jobpulse -p 5432:5432 postgres:15-alpine
```

**Option B: Local Install**
- Windows: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
- Mac: `brew install postgresql@15`
- Linux: `sudo apt-get install postgresql-15`

Create the database:
```bash
psql -U postgres
CREATE DATABASE jobpulse;
CREATE USER jobpulse WITH PASSWORD 'jobpulse_secret';
GRANT ALL PRIVILEGES ON DATABASE jobpulse TO jobpulse;
```

### 4. Redis

**Option A: Docker (Recommended)**
```bash
docker run -d --name jobpulse-redis -p 6379:6379 redis:7-alpine
```

**Option B: Local Install**
- Windows: Use WSL or Docker
- Mac: `brew install redis`
- Linux: `sudo apt-get install redis-server`

## Configuration

### Backend Environment Variables

Copy and edit `backend/.env`:

```env
DATABASE_URL=postgresql://jobpulse:jobpulse_secret@localhost:5432/jobpulse
REDIS_URL=redis://localhost:6379/0

# Supabase (create project at https://supabase.com)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Razorpay (get keys at https://dashboard.razorpay.com)
RAZORPAY_KEY_ID=rzp_test_xxxxx
RAZORPAY_KEY_SECRET=xxxxx
RAZORPAY_WEBHOOK_SECRET=xxxxx

# OpenAI (get key at https://platform.openai.com)
OPENAI_API_KEY=sk-xxxxx

# Hunter.io (get key at https://hunter.io)
HUNTER_IO_API_KEY=xxxxx

# Bright Data (get proxy at https://brightdata.com)
BRIGHT_DATA_PROXY=http://brd-customer-xxxxx:xxxxx@zproxy.lum-superproxy.io:22225
```

### Frontend Environment Variables

Copy and edit `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

## Running the Application

### Option A: Docker (All-in-One)

```bash
docker compose up -d

# Run database migrations
docker exec jobpulse-api alembic upgrade head
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Option B: Manual (Development)

Terminal 1 - Backend:
```bash
cd backend
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Mac/Linux

# Run migrations
alembic upgrade head

# Start API server
uvicorn app.main:app --reload --port 8000
```

Terminal 2 - Celery Worker:
```bash
cd backend
venv\Scripts\activate
celery -A workers.celery_app worker --loglevel=info --concurrency=4
```

Terminal 3 - Celery Beat (Scheduler):
```bash
cd backend
venv\Scripts\activate
celery -A workers.celery_app beat --loglevel=info
```

Terminal 4 - Frontend:
```bash
cd frontend
npm run dev
```

## Troubleshooting

### Python not found
- Windows: Add Python to PATH manually or reinstall with "Add to PATH" checked
- Verify: `python --version`

### Node.js not found
- Verify: `node --version`
- Reinstall from https://nodejs.org/

### PostgreSQL connection refused
- Check if PostgreSQL is running: `docker ps` or `pg_isready`
- Verify credentials in `.env` match your setup

### Redis connection refused
- Check if Redis is running: `docker ps` or `redis-cli ping`
- Expected response: `PONG`

### Playwright browser not found
```bash
playwright install chromium
playwright install-deps
```

### CORS errors
- Ensure `NEXT_PUBLIC_API_URL` in frontend `.env.local` matches backend URL
- Check backend CORS settings in `app/main.py`

## Production Deployment

### AWS Mumbai Region

1. **Database**: Use Amazon RDS PostgreSQL in ap-south-1
2. **Redis**: Use Amazon ElastiCache in ap-south-1
3. **Backend**: Deploy to AWS ECS or EC2
4. **Frontend**: Deploy to Vercel or AWS Amplify
5. **Environment**: Set all `.env` variables in your deployment platform

### Docker Production Build

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

## API Keys Setup

### Supabase
1. Create project at https://supabase.com
2. Go to Project Settings > API
3. Copy `URL`, `anon public key`, and `service_role key`

### Razorpay
1. Create account at https://dashboard.razorpay.com
2. Go to Settings > API Keys
3. Generate test keys
4. Set up webhook endpoint: `https://your-domain.com/api/v1/webhooks/razorpay`

### OpenAI
1. Create account at https://platform.openai.com
2. Go to API Keys
3. Create new secret key

### Hunter.io
1. Create account at https://hunter.io
2. Go to Account Settings > API
3. Copy your API key

### Bright Data
1. Create account at https://brightdata.com
2. Create a Residential Proxy zone
3. Copy the proxy URL format
