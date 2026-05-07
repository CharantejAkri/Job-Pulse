#!/bin/bash
# JobPulse Docker Healthcheck Script
# Checks if all containers are healthy and endpoints respond

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASS=0
FAIL=0

check_service() {
    local name=$1
    local url=$2
    local expected=$3

    response=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "$url" 2>/dev/null || echo "000")

    if [ "$response" = "$expected" ]; then
        echo -e "${GREEN}[PASS]${NC} $name ($response)"
        PASS=$((PASS + 1))
    else
        echo -e "${RED}[FAIL]${NC} $name (Expected $expected, got $response)"
        FAIL=$((FAIL + 1))
    fi
}

echo "========================================"
echo "  JobPulse Docker Healthcheck"
echo "========================================"
echo ""

echo "Checking container status..."
echo ""

# Check containers are running
for container in jobpulse-api jobpulse-frontend jobpulse-db jobpulse-redis; do
    status=$(docker ps --filter "name=$container" --format "{{.Status}}" 2>/dev/null)
    if echo "$status" | grep -q "Up"; then
        echo -e "${GREEN}[RUNNING]${NC} $container"
    else
        echo -e "${RED}[DOWN]${NC} $container"
        FAIL=$((FAIL + 1))
    fi
done

echo ""

# Check API health
echo "Checking API endpoints..."
check_service "Backend API" "http://localhost:8000/health" "200"
check_service "Health Detail" "http://localhost:8000/health/detail" "200"
check_service "Frontend" "http://localhost:3000" "200"
check_service "API Docs" "http://localhost:8000/docs" "200"

echo ""
echo "========================================"
echo "  Results: ${GREEN}$PASS passed${NC}, ${RED}$FAIL failed${NC}"
echo "========================================"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi

exit 0
