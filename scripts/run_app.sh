#!/bin/bash

# Professional run script for CrewAI YouTube Summarizer & Academic Assistant
# Usage: ./scripts/run_app.sh [professional|simple]

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project directory
PROJECT_DIR="/media/professor/New Volume/Internship-szl/crew-ai"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if virtual environment exists
check_venv() {
    if [ ! -d "$PROJECT_DIR/.venv" ]; then
        print_error "Virtual environment not found!"
        print_status "Creating virtual environment..."
        cd "$PROJECT_DIR"
        python3 -m venv .venv
        print_success "Virtual environment created!"
    fi
}

# Function to activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    cd "$PROJECT_DIR"
    source .venv/bin/activate
    print_success "Virtual environment activated!"
}

# Function to install dependencies
install_deps() {
    print_status "Checking dependencies..."
    if ! pip show streamlit > /dev/null 2>&1; then
        print_status "Installing dependencies..."
        pip install -r requirements.txt
        print_success "Dependencies installed!"
    else
        print_success "Dependencies already installed!"
    fi
}

# Function to check API key
check_api_key() {
    if [ -f "$PROJECT_DIR/.env" ]; then
        if grep -q "GROQ_API_KEY=your_groq_api_key_here" "$PROJECT_DIR/.env"; then
            print_warning "Please update your Groq API key in the .env file!"
            print_status "Get your API key from: https://console.groq.com"
        else
            print_success "API key configuration found!"
        fi
    else
        print_warning "No .env file found. You'll need to enter your API key in the UI."
    fi
}

# Function to run the application
run_app() {
    local version=${1:-"simple"}
    
    print_status "Starting CrewAI YouTube Summarizer & Academic Assistant..."
    print_status "Version: $version"
    print_status "Opening browser at: http://localhost:8501"
    
    case $version in
        "professional")
            streamlit run main.py
            ;;
        "simple")
            streamlit run app_working.py
            ;;
        *)
            print_error "Invalid version. Use 'professional' or 'simple'"
            exit 1
            ;;
    esac
}

# Main execution
main() {
    echo "=================================================="
    echo "  CrewAI YouTube Summarizer & Academic Assistant"
    echo "=================================================="
    echo ""
    
    # Check if project directory exists
    if [ ! -d "$PROJECT_DIR" ]; then
        print_error "Project directory not found: $PROJECT_DIR"
        exit 1
    fi
    
    # Setup environment
    check_venv
    activate_venv
    install_deps
    check_api_key
    
    echo ""
    print_status "Setup complete! Starting application..."
    echo ""
    
    # Run the application
    run_app $1
}

# Execute main function with all arguments
main "$@"
