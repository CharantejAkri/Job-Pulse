.PHONY: help setup backend frontend docker db redis migrate clean test

help:
	@echo "JobPulse India - Makefile Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup        - Run setup script for your OS"
	@echo "  make verify       - Check if all prerequisites are installed"
	@echo ""
	@echo "Development:"
	@echo "  make backend      - Start FastAPI backend"
	@echo "  make frontend     - Start Next.js frontend"
	@echo "  make worker       - Start Celery worker"
	@echo "  make beat         - Start Celery beat scheduler"
	@echo "  make dev          - Start all services (backend, frontend, worker)"
	@echo ""
	@echo "Docker:"
	@echo "  make docker       - Start all services with Docker"
	@echo "  make docker-down  - Stop Docker services"
	@echo "  make docker-logs  - View Docker logs"
	@echo ""
	@echo "Database:"
	@echo "  make db           - Start PostgreSQL with Docker"
	@echo "  make redis        - Start Redis with Docker"
	@echo "  make migrate      - Run database migrations"
	@echo "  make migrate-new  - Create new migration (usage: make migrate-new msg='add_column')"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        - Remove virtual env, node_modules, build files"

# Setup
setup:
ifeq ($(OS),Windows_NT)
	powershell -ExecutionPolicy Bypass -File setup.ps1
else
	chmod +x setup.sh && ./setup.sh
endif

verify:
	@echo "Checking prerequisites..."
	@python --version 2>/dev/null || echo "  Python: NOT FOUND"
	@node --version 2>/dev/null || echo "  Node.js: NOT FOUND"
	@docker --version 2>/dev/null || echo "  Docker: NOT FOUND"
	@psql --version 2>/dev/null || echo "  PostgreSQL: NOT FOUND"
	@redis-cli ping 2>/dev/null || echo "  Redis: NOT FOUND"
	@echo ""
	@echo "Setup complete if all tools found above."

# Backend
backend:
	cd backend && uvicorn app.main:app --reload --port 8000

# Frontend
frontend:
	cd frontend && npm run dev

# Celery Worker
worker:
	cd backend && celery -A workers.celery_app worker --loglevel=info --concurrency=4

# Celery Beat
beat:
	cd backend && celery -A workers.celery_app beat --loglevel=info

# Dev (all services)
dev:
	@echo "Starting all services..."
	@echo "Open 4 terminal tabs and run:"
	@echo "  Terminal 1: make backend"
	@echo "  Terminal 2: make frontend"
	@echo "  Terminal 3: make worker"
	@echo "  Terminal 4: make beat"

# Docker
docker:
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

docker-build:
	docker compose up -d --build

# Database
db:
	docker run -d --name jobpulse-db -e POSTGRES_USER=jobpulse -e POSTGRES_PASSWORD=jobpulse_secret -e POSTGRES_DB=jobpulse -p 5432:5432 postgres:15-alpine

redis:
	docker run -d --name jobpulse-redis -p 6379:6379 redis:7-alpine

migrate:
	cd backend && alembic upgrade head

migrate-new:
	cd backend && alembic revision --autogenerate -m "$(msg)"

# Cleanup
clean:
	rm -rf backend/venv backend/__pycache__ backend/.pytest_cache
	rm -rf frontend/node_modules frontend/.next
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaned up build artifacts."
