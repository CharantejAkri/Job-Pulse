# JobPulse India - Setup Script (Windows)
# Run this script in PowerShell to install all prerequisites

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  JobPulse India - Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "Warning: Some installations may require Administrator privileges." -ForegroundColor Yellow
    Write-Host "If installation fails, re-run this script as Administrator." -ForegroundColor Yellow
    Write-Host ""
}

# Function to check if a command exists
function Test-Command($cmd) {
    $null -ne (Get-Command $cmd -ErrorAction SilentlyContinue)
}

# Step 1: Install Python
Write-Host "[1/5] Checking Python..." -ForegroundColor Yellow
if (Test-Command "python") {
    $pythonVersion = python --version 2>&1
    Write-Host "  Found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  Python not found. Installing Python 3.11..." -ForegroundColor Yellow
    winget install Python.Python.3.11 --accept-source-agreements --accept-package-agreements
    Write-Host "  Python installed. Please restart your terminal for changes to take effect." -ForegroundColor Green
}

# Step 2: Install Node.js
Write-Host "[2/5] Checking Node.js..." -ForegroundColor Yellow
if (Test-Command "node") {
    $nodeVersion = node --version
    Write-Host "  Found: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "  Node.js not found. Installing Node.js LTS..." -ForegroundColor Yellow
    winget install OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements
    Write-Host "  Node.js installed. Please restart your terminal for changes to take effect." -ForegroundColor Green
}

# Step 3: Install PostgreSQL (Optional - for local DB)
Write-Host "[3/5] Checking PostgreSQL..." -ForegroundColor Yellow
if (Test-Command "psql") {
    Write-Host "  PostgreSQL found." -ForegroundColor Green
} else {
    Write-Host "  PostgreSQL not found." -ForegroundColor Yellow
    $installPg = Read-Host "  Install PostgreSQL 15 locally? (y/n) - Skip if using Docker"
    if ($installPg -eq "y") {
        winget install PostgreSQL.PostgreSQL.15 --accept-source-agreements --accept-package-agreements
        Write-Host "  PostgreSQL installed." -ForegroundColor Green
    } else {
        Write-Host "  Skipping PostgreSQL. You'll need Docker or a remote DB." -ForegroundColor Yellow
    }
}

# Step 4: Install Redis (Optional - for local queue)
Write-Host "[4/5] Checking Redis..." -ForegroundColor Yellow
if (Test-Command "redis-server") {
    Write-Host "  Redis found." -ForegroundColor Green
} else {
    Write-Host "  Redis not found." -ForegroundColor Yellow
    $installRedis = Read-Host "  Install Redis via Docker? (y/n) - Requires Docker Desktop"
    if ($installRedis -eq "y") {
        if (Test-Command "docker") {
            docker run -d --name jobpulse-redis -p 6379:6379 redis:7-alpine
            Write-Host "  Redis container started." -ForegroundColor Green
        } else {
            Write-Host "  Docker not found. Install Docker Desktop first." -ForegroundColor Red
        }
    } else {
        Write-Host "  Skipping Redis. You'll need Docker or a remote Redis instance." -ForegroundColor Yellow
    }
}

# Step 5: Install Docker (Optional - recommended for easiest setup)
Write-Host "[5/5] Checking Docker..." -ForegroundColor Yellow
if (Test-Command "docker") {
    $dockerVersion = docker --version
    Write-Host "  Found: $dockerVersion" -ForegroundColor Green
} else {
    Write-Host "  Docker not found." -ForegroundColor Yellow
    $installDocker = Read-Host "  Install Docker Desktop? (y/n) - Recommended for easiest setup"
    if ($installDocker -eq "y") {
        winget install Docker.DockerDesktop --accept-source-agreements --accept-package-agreements
        Write-Host "  Docker Desktop installed. Please restart your computer." -ForegroundColor Green
    } else {
        Write-Host "  Skipping Docker. You'll need to run services manually." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "1. Restart your terminal (required for Python/Node.js to be recognized)" -ForegroundColor White
Write-Host "2. Copy environment files:" -ForegroundColor White
Write-Host "   copy backend\.env.example backend\.env" -ForegroundColor Gray
Write-Host "   copy frontend\.env.example frontend\.env.local" -ForegroundColor Gray
Write-Host "3. Edit .env files with your API keys" -ForegroundColor White
Write-Host "4. Run the app:" -ForegroundColor White
Write-Host "   Option A (Docker): docker compose up -d" -ForegroundColor Gray
Write-Host "   Option B (Manual): See SETUP.md for instructions" -ForegroundColor Gray
Write-Host ""
