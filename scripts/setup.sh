#!/bin/bash

# Setup script for CrewAI YouTube Summarizer & Academic Assistant
# This script sets up the complete development environment

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "  CrewAI Project Setup"
echo "=========================================="

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
python3 --version

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
python3 -m venv .venv

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source .venv/bin/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${BLUE}Creating .env file...${NC}"
    cp .env .env.backup 2>/dev/null || true
    echo "GROQ_API_KEY=your_groq_api_key_here" > .env
fi

echo -e "${GREEN}Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Get your Groq API key from: https://console.groq.com"
echo "2. Edit .env file and add your API key"
echo "3. Run: ./scripts/run_app.sh simple"
echo ""
