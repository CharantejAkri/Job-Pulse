# JobPulse India - Production Deployment Guide

## Prerequisites

Before users can access the app, you need these 6 things:

### 1. A Server (Ubuntu 22.04+)
- **Minimum:** 2 vCPU, 4GB RAM, 50GB SSD
- **Recommended:** AWS t3.medium (Mumbai region `ap-south-1`)
- Open ports: **22** (SSH), **80** (HTTP), **443** (HTTPS)

### 2. A Domain Name
- e.g., `jobpulse.in` or `app.jobpulse.in`
- Point DNS A record to your server IP
- Required for Razorpay webhooks + Google OAuth redirects

### 3. Supabase Project (Free tier works)
1. Create account at https://supabase.com
2. Create a new project (select Mumbai region if available)
3. Enable **Google OAuth** in Authentication > Providers
4. Get these from Project Settings > API:
   - `Project URL`
   - `anon public key`
   - `service_role key` (keep secret!)

### 4. Razorpay Account
1. Register at https://dashboard.razorpay.com
2. Get API keys from Settings > API Keys
3. Set up webhook endpoint:
   - URL: `https://your-domain.com/api/v1/webhooks/razorpay`
   - Events: `subscription.charged`, `payment.captured`, `subscription.cancelled`
4. Create subscription plans in Razorpay Dashboard:
   - Pro: ₹1,499/month (500 credits)
   - Agency: ₹4,999/month (2,500 credits)
5. Copy plan IDs into `backend/app/api/v1/subscriptions.py`

### 5. OpenAI API Key
1. https://platform.openai.com/api-keys
2. Create a key with access to `gpt-4o-mini`

### 6. Hunter.io API Key
1. https://hunter.io/account
2. Copy your API key (free tier allows 25 searches/month)

---

## Quick Start (Fresh Ubuntu Server)

```bash
# SSH into your server
ssh ubuntu@your-server-ip

# Download and run deploy script
wget -O deploy.sh https://raw.githubusercontent.com/yourorg/jobpulse/main/scripts/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

The script installs Docker, clones the repo, and starts everything.

---

## Manual Deployment

### Step 1: Install Docker + Dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose-v2 nginx certbot python3-certbot-nginx
sudo systemctl enable docker
sudo systemctl start docker
```

### Step 2: Clone & Configure

```bash
git clone https://github.com/yourorg/jobpulse.git /opt/jobpulse
cd /opt/jobpulse

# Create production env file
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
```

Edit `backend/.env` with all API keys (see checklist above).

### Step 3: Start with Production Docker Compose

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

### Step 4: Set Up SSL with Certbot

```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### Step 5: Configure Nginx as Reverse Proxy

Create `/etc/nginx/sites-available/jobpulse`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com www.your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/jobpulse /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

---

## Verifying the Deployment

```bash
# Check all containers are healthy
./scripts/docker-healthcheck.sh

# Check API health
curl https://your-domain.com/health
# Expected: {"status":"ok","version":"1.0.0"}

# Check detailed health
curl https://your-domain.com/health/detail
# Expected: {"status":"healthy","checks":{"database":{"status":"connected"},...}}
```

---

## Monitoring & Maintenance

### Logs
```bash
# View all logs
docker compose logs -f

# View specific service
docker compose logs -f backend
docker compose logs -f frontend
```

### Backups
```bash
# Backup PostgreSQL database
docker exec jobpulse-db pg_dump -U jobpulse jobpulse > backup_$(date +%F).sql
```

### Updates
```bash
cd /opt/jobpulse
git pull
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Containers won't start | Check `docker compose logs` for errors |
| CORS errors | Verify `NEXT_PUBLIC_API_URL` in frontend `.env` |
| Razorpay webhook fails | Ensure domain uses HTTPS + correct webhook secret |
| LinkedIn blocks scraper | Check Bright Data proxy is active + rotating IPs |
| Email not found | Hunter.io free tier limited; upgrade for more queries |
| Database connection failed | Verify `DATABASE_URL` in `backend/.env` |
| SSL cert expired | `sudo certbot renew` |