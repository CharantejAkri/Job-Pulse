#!/bin/bash
# JobPulse India - Environment Verification Script (Linux/Mac)
# Run: chmod +x verify.sh && ./verify.sh

echo "========================================"
echo "  JobPulse - Environment Check"
echo "========================================"
echo ""

all_passed=true

# Check Python
printf "[1/6] Python... "
if command -v python3 &>/dev/null; then
    python_version=$(python3 --version 2>&1)
    if echo "$python_version" | grep -qE "Python 3\.(1[1-9]|[2-9][0-9])"; then
        echo "PASS ($python_version)"
    else
        echo "FAIL (Need Python 3.11+, found: $python_version)"
        all_passed=false
    fi
else
    echo "FAIL (Not installed)"
    all_passed=false
fi

# Check Node.js
printf "[2/6] Node.js... "
if command -v node &>/dev/null; then
    node_version=$(node --version 2>&1)
    node_major=$(echo "$node_version" | sed 's/v\([0-9]*\)\..*/\1/')
    if [ "$node_major" -ge 18 ]; then
        echo "PASS ($node_version)"
    else
        echo "FAIL (Need Node 18+, found: $node_version)"
        all_passed=false
    fi
else
    echo "FAIL (Not installed)"
    all_passed=false
fi

# Check npm
printf "[3/6] npm... "
if command -v npm &>/dev/null; then
    npm_version=$(npm --version 2>&1)
    echo "PASS (v$npm_version)"
else
    echo "FAIL (Not installed)"
    all_passed=false
fi

# Check PostgreSQL
printf "[4/6] PostgreSQL... "
if command -v psql &>/dev/null; then
    pg_version=$(psql --version 2>&1)
    echo "PASS ($pg_version)"
else
    echo "FAIL (Not installed - needed for local dev)"
fi

# Check Redis
printf "[5/6] Redis... "
if command -v redis-cli &>/dev/null; then
    redis_ping=$(redis-cli ping 2>&1)
    if [ "$redis_ping" = "PONG" ]; then
        echo "PASS (Running)"
    else
        echo "FAIL (Not running)"
    fi
elif command -v docker &>/dev/null; then
    docker_redis=$(docker ps --filter "name=jobpulse-redis" --format "{{.Names}}" 2>&1)
    if [ "$docker_redis" = "jobpulse-redis" ]; then
        echo "PASS (Running in Docker)"
    else
        echo "FAIL (Not running)"
    fi
else
    echo "FAIL (Not installed)"
fi

# Check Docker
printf "[6/6] Docker... "
if command -v docker &>/dev/null; then
    docker_version=$(docker --version 2>&1)
    echo "PASS ($docker_version)"
else
    echo "FAIL (Not installed - recommended for easiest setup)"
fi

echo ""
echo "========================================"

if [ "$all_passed" = true ]; then
    echo "  All core prerequisites installed!"
    echo "========================================"
    echo ""
    echo "Next: Copy .env files and fill in API keys"
    echo "  cp backend/.env.example backend/.env"
    echo "  cp frontend/.env.example frontend/.env.local"
else
    echo "  Some prerequisites missing."
    echo "========================================"
    echo ""
    echo "Run setup.sh to install missing tools:"
    echo "  ./setup.sh"
fi

echo ""
