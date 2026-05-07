#!/bin/bash
# JobPulse India - Ubuntu Server Deploy Script
# Usage: curl -fsSL https://raw.githubusercontent.com/yourorg/jobpulse/main/scripts/deploy.sh | bash
# Or: wget -qO- https://bit.ly/jobpulse-deploy | bash

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo "========================================"
echo "  JobPulse India - Server Deployment"
echo "========================================"
echo ""

# --- Config ---
REPO_URL=${REPO_URL:-"https://github.com/yourorg/jobpulse.git"}
INSTALL_DIR=${INSTALL_DIR:-"/opt/jobpulse"}
DOMAIN=${DOMAIN:-""}

# --- Step 1: Update system ---
echo -e "${YELLOW}[1/7] Updating system packages...${NC}"
sudo apt update && sudo apt upgrade -y

# --- Step 2: Install Docker ---
echo -e "${YELLOW}[2/7] Installing Docker...${NC}"
if ! command -v docker &>/dev/null; then
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
    echo -e "${GREEN}  Docker installed. You may need to re-login for group changes.${NC}"
else
    echo -e "${GREEN}  Docker already installed.${NC}"
fi

# --- Step 3: Install Docker Compose ---
echo -e "${YELLOW}[3/7] Installing Docker Compose...${NC}"
if ! command -v docker-compose &>/dev/null && ! docker compose version &>/dev/null; then
    sudo apt install -y docker-compose-v2
else
    echo -e "${GREEN}  Docker Compose already installed.${NC}"
fi

# --- Step 4: Install Nginx + Certbot ---
echo -e "${YELLOW}[4/7] Installing Nginx & Certbot...${NC}"
sudo apt install -y nginx certbot python3-certbot-nginx

# --- Step 5: Clone repository ---
echo -e "${YELLOW}[5/7] Cloning JobPulse repository...${NC}"
if [ -d "$INSTALL_DIR" ]; then
    echo -e "  Updating existing installation at $INSTALL_DIR"
    cd $INSTALL_DIR && sudo git pull
else
    sudo git clone $REPO_URL $INSTALL_DIR
fi
cd $INSTALL_DIR

# --- Step 6: Configure environment ---
echo -e "${YELLOW}[6/7] Setting up environment files...${NC}"
if [ ! -f "backend/.env" ]; then
    sudo cp backend/.env.example backend/.env
    echo -e "${RED}  !!! EDIT backend/.env with your API keys !!!${NC}"
    echo -e "${RED}      nano $INSTALL_DIR/backend/.env${NC}"
fi
if [ ! -f "frontend/.env.local" ]; then
    sudo cp frontend/.env.example frontend/.env.local
fi

# --- Step 7: Start services ---
echo -e "${YELLOW}[7/7] Starting Docker services...${NC}"
sudo docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

# --- Verify ---
echo ""
echo -e "${CYAN}Waiting for services to start...${NC}"
sleep 10

echo ""
echo "========================================"
echo -e "${GREEN}  Deployment Complete!${NC}"
echo "========================================"
echo ""
echo "  Next steps:"
echo "  1. Edit API keys: nano $INSTALL_DIR/backend/.env"
echo "  2. Restart: cd $INSTALL_DIR && sudo docker compose restart"
echo "  3. Set up SSL: sudo certbot --nginx -d $DOMAIN"
echo ""

# --- Check health ---
echo "  Checking API health..."
if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}  API: Running ✓${NC}"
else
    echo -e "${RED}  API: Not responding (check docker compose logs)${NC}"
fi

if curl -sf http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}  Frontend: Running ✓${NC}"
else
    echo -e "${RED}  Frontend: Not responding (check docker compose logs)${NC}"
fi

echo ""
echo "  Access the app at:"
echo -e "${CYAN}  http://your-server-ip${NC}"
echo ""

# --- Print commands to remember ---
echo -e "${YELLOW}Useful commands:${NC}"
echo "  sudo docker compose logs -f    # View logs"
echo "  sudo docker compose restart    # Restart all services"
echo "  sudo docker compose pull       # Update images"
echo ""
