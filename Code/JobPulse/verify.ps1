# JobPulse India - Environment Verification Script
# Run this after setup to verify all prerequisites are installed

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  JobPulse - Environment Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allPassed = $true

# Check Python
Write-Host "[1/6] Python..." -NoNewline
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3\.(1[1-9]|[2-9][0-9])") {
        Write-Host " PASS ($pythonVersion)" -ForegroundColor Green
    } else {
        Write-Host " FAIL (Need Python 3.11+, found: $pythonVersion)" -ForegroundColor Red
        $allPassed = $false
    }
} catch {
    Write-Host " FAIL (Not installed)" -ForegroundColor Red
    $allPassed = $false
}

# Check Node.js
Write-Host "[2/6] Node.js..." -NoNewline
try {
    $nodeVersion = node --version 2>&1
    $nodeMajor = [int]($nodeVersion -replace 'v(\d+)\..*', '$1')
    if ($nodeMajor -ge 18) {
        Write-Host " PASS ($nodeVersion)" -ForegroundColor Green
    } else {
        Write-Host " FAIL (Need Node 18+, found: $nodeVersion)" -ForegroundColor Red
        $allPassed = $false
    }
} catch {
    Write-Host " FAIL (Not installed)" -ForegroundColor Red
    $allPassed = $false
}

# Check npm
Write-Host "[3/6] npm..." -NoNewline
try {
    $npmVersion = npm --version 2>&1
    Write-Host " PASS (v$npmVersion)" -ForegroundColor Green
} catch {
    Write-Host " FAIL (Not installed)" -ForegroundColor Red
    $allPassed = $false
}

# Check PostgreSQL
Write-Host "[4/6] PostgreSQL..." -NoNewline
try {
    $pgVersion = psql --version 2>&1
    Write-Host " PASS ($pgVersion)" -ForegroundColor Green
} catch {
    Write-Host " FAIL (Not installed - needed for local dev)" -ForegroundColor Yellow
}

# Check Redis
Write-Host "[5/6] Redis..." -NoNewline
try {
    $redisPing = redis-cli ping 2>&1
    if ($redisPing -eq "PONG") {
        Write-Host " PASS (Running)" -ForegroundColor Green
    } else {
        Write-Host " FAIL (Not running)" -ForegroundColor Yellow
    }
} catch {
    try {
        $dockerRedis = docker ps --filter "name=jobpulse-redis" --format "{{.Names}}" 2>&1
        if ($dockerRedis -eq "jobpulse-redis") {
            Write-Host " PASS (Running in Docker)" -ForegroundColor Green
        } else {
            Write-Host " FAIL (Not running)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host " FAIL (Not installed)" -ForegroundColor Yellow
    }
}

# Check Docker
Write-Host "[6/6] Docker..." -NoNewline
try {
    $dockerVersion = docker --version 2>&1
    Write-Host " PASS ($dockerVersion)" -ForegroundColor Green
} catch {
    Write-Host " FAIL (Not installed - recommended for easiest setup)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($allPassed) {
    Write-Host "  All core prerequisites installed!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next: Copy .env files and fill in API keys" -ForegroundColor White
    Write-Host "  copy backend\.env.example backend\.env" -ForegroundColor Gray
    Write-Host "  copy frontend\.env.example frontend\.env.local" -ForegroundColor Gray
} else {
    Write-Host "  Some prerequisites missing." -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Run setup.ps1 to install missing tools:" -ForegroundColor White
    Write-Host "  .\setup.ps1" -ForegroundColor Gray
}

Write-Host ""
