#!/bin/bash
# JobPulse India - Setup Script (Linux/Mac)
# Run: chmod +x setup.sh && ./setup.sh

echo "========================================"
echo "  JobPulse India - Setup Script"
echo "========================================"
echo ""

# Check OS
OS="$(uname -s)"
echo "Detected OS: $OS"
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Install Python
echo "[1/5] Checking Python..."
if command_exists python3; then
    echo "  Found: $(python3 --version)"
else
    echo "  Python not found. Installing..."
    if [ "$OS" = "Darwin" ]; then
        brew install python@3.11
    elif command_exists apt-get; then
        sudo apt-get update && sudo apt-get install -y python3.11 python3.11-venv python3-pip
    elif command_exists yum; then
        sudo yum install -y python3.11
    elif command_exists pacman; then
        sudo pacman -S python
    fi
    echo "  Python installed."
fi

# Step 2: Install Node.js
echo "[2/5] Checking Node.js..."
if command_exists node; then
    echo "  Found: $(node --version)"
else
    echo "  Node.js not found. Installing..."
    if [ "$OS" = "Darwin" ]; then
        brew install node
    elif command_exists curl; then
        curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
        sudo apt-get install -y nodejs
    fi
    echo "  Node.js installed."
fi

# Step 3: Install PostgreSQL
echo "[3/5] Checking PostgreSQL..."
if command_exists psql; then
    echo "  PostgreSQL found."
else
    echo "  PostgreSQL not found."
    read -p "  Install PostgreSQL 15? (y/n) " install_pg
    if [ "$install_pg" = "y" ]; then
        if [ "$OS" = "Darwin" ]; then
            brew install postgresql@15
        elif command_exists apt-get; then
            sudo apt-get install -y postgresql-15
        fi
        echo "  PostgreSQL installed."
    else
        echo "  Skipping PostgreSQL. You'll need Docker or a remote DB."
    fi
fi

# Step 4: Install Redis
echo "[4/5] Checking Redis..."
if command_exists redis-server; then
    echo "  Redis found."
else
    echo "  Redis not found."
    read -p "  Install Redis? (y/n) " install_redis
    if [ "$install_redis" = "y" ]; then
        if [ "$OS" = "Darwin" ]; then
            brew install redis
        elif command_exists apt-get; then
            sudo apt-get install -y redis-server
        fi
        echo "  Redis installed."
    else
        echo "  Skipping Redis. You'll need Docker or a remote Redis instance."
    fi
fi

# Step 5: Install Docker
echo "[5/5] Checking Docker..."
if command_exists docker; then
    echo "  Found: $(docker --version)"
else
    echo "  Docker not found."
    read -p "  Install Docker? (y/n) " install_docker
    if [ "$install_docker" = "y" ]; then
        if [ "$OS" = "Darwin" ]; then
            echo "  Please download Docker Desktop from: https://www.docker.com/products/docker-desktop"
        elif command_exists apt-get; then
            curl -fsSL https://get.docker.com | sh
            sudo usermod -aG docker $USER
        fi
        echo "  Docker installed. Please restart your terminal."
    else
        echo "  Skipping Docker. You'll need to run services manually."
    fi
fi

echo ""
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Copy environment files:"
echo "   cp backend/.env.example backend/.env"
echo "   cp frontend/.env.example frontend/.env.local"
echo "2. Edit .env files with your API keys"
echo "3. Run the app:"
echo "   Option A (Docker): docker compose up -d"
echo "   Option B (Manual): See SETUP.md for instructions"
echo ""
