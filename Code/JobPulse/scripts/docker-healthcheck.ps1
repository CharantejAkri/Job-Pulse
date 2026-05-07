# JobPulse Docker Healthcheck Script (Windows PowerShell)
# Checks if all containers are healthy and endpoints respond

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  JobPulse Docker Healthcheck" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$pass = 0
$fail = 0

# Check containers are running
Write-Host "Checking container status..." -ForegroundColor Yellow
Write-Host ""

$containers = @("jobpulse-api", "jobpulse-frontend", "jobpulse-db", "jobpulse-redis")

foreach ($container in $containers) {
    try {
        $status = docker ps --filter "name=$container" --format "{{.Status}}" 2>$null
        if ($status -match "Up") {
            Write-Host "[RUNNING] $container" -ForegroundColor Green
        } else {
            Write-Host "[DOWN] $container" -ForegroundColor Red
            $fail++
        }
    } catch {
        Write-Host "[DOWN] $container" -ForegroundColor Red
        $fail++
    }
}

Write-Host ""

# Check API endpoints
Write-Host "Checking API endpoints..." -ForegroundColor Yellow
Write-Host ""

function Check-Service($name, $url, $expected) {
    try {
        $response = Invoke-WebRequest -Uri $url -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq $expected) {
            Write-Host "[PASS] $name ($($response.StatusCode))" -ForegroundColor Green
            $script:pass++
        } else {
            Write-Host "[FAIL] $name (Expected $expected, got $($response.StatusCode))" -ForegroundColor Red
            $script:fail++
        }
    } catch {
        Write-Host "[FAIL] $name (No response)" -ForegroundColor Red
        $script:fail++
    }
}

Check-Service "Backend API" "http://localhost:8000/health" 200
Check-Service "Health Detail" "http://localhost:8000/health/detail" 200
Check-Service "Frontend" "http://localhost:3000" 200
Check-Service "API Docs" "http://localhost:8000/docs" 200

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Results: $pass passed, $fail failed" -ForegroundColor $(if ($fail -eq 0) { "Green" } else { "Red" })
Write-Host "========================================" -ForegroundColor Cyan

if ($fail -gt 0) {
    exit 1
}
