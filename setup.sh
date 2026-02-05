#!/bin/bash

# Quick Start Script for Fagskolen Viken AI Study Advisor
# This script helps set up and run the complete system

set -e  # Exit on error

echo "========================================"
echo "Fagskolen Viken - AI Study Advisor"
echo "Quick Start Setup Script"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}!${NC} $1"
}

# Check prerequisites
echo "Checking prerequisites..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python 3 found: $PYTHON_VERSION"
else
    print_error "Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check Docker
if command -v docker &> /dev/null; then
    print_status "Docker found"
else
    print_error "Docker is not installed. Please install Docker."
    exit 1
fi

# Check Docker Compose
if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
    print_status "Docker Compose found"
else
    print_error "Docker Compose is not installed. Please install Docker Compose."
    exit 1
fi

echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt || {
    print_error "Failed to install Python dependencies"
    exit 1
}
print_status "Python dependencies installed"

echo ""
echo "Starting MySQL database..."
cd MySQL
docker-compose up -d || {
    print_error "Failed to start MySQL database"
    exit 1
}
cd ..
print_status "MySQL database started"

echo ""
echo "Waiting for MySQL to be ready..."
sleep 10

echo ""
echo "Creating database schema..."
cd Scraping
python3 create_database.py || {
    print_warning "Failed to create database schema (database might already exist)"
}
cd ..
print_status "Database schema ready"

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Run the web scraping pipeline:"
echo "   cd Scraping"
echo "   python3 main.py"
echo ""
echo "2. Start the MCP server:"
echo "   cd FastMCP_server"
echo "   python3 mcp_server.py"
echo ""
echo "3. Configure and run the agent:"
echo "   cd fagskolen_agent"
echo "   # Create .env file with your GOOGLE_API_KEY"
echo "   python3 agent.py"
echo ""
echo "For more details, see README.md"
echo ""
