#!/bin/bash

# =============================================================================
# RAG Production System - Quick Setup Script
# =============================================================================
# 
# This script helps you quickly set up the RAG system for development
# and production deployment.
# 
# Author: [Your Name]
# Project: RAG Production System
# Version: 1.0.0
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Docker installation
check_docker() {
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        print_status "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        print_status "Visit: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Function to setup environment file
setup_env() {
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            print_status "Creating .env file from template..."
            cp .env.example .env
            print_warning "Please edit .env file with your actual API keys and configuration"
            print_status "Required: GROQ_API_KEY, QDRANT_API_KEY, SECRET_KEY"
        else
            print_error ".env.example file not found. Please create .env file manually."
            exit 1
        fi
    else
        print_success ".env file already exists"
    fi
}

# Function to create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    mkdir -p uploads
    mkdir -p logs
    mkdir -p qdrant_data
    mkdir -p qdrant_snapshots
    print_success "Directories created successfully"
}

# Function to start services
start_services() {
    print_status "Starting RAG system services..."
    
    # Create Docker network if it doesn't exist
    if ! docker network ls | grep -q rag-network; then
        print_status "Creating Docker network..."
        docker network create rag-network
    fi
    
    # Start services with Docker Compose
    print_status "Starting services with Docker Compose..."
    docker-compose up -d
    
    print_success "Services started successfully!"
    print_status "Waiting for services to be ready..."
    
    # Wait for services to be healthy
    sleep 30
    
    # Check service status
    print_status "Checking service status..."
    docker-compose ps
    
    print_success "Setup completed successfully!"
    print_status "Access your RAG system at: http://localhost:8000"
    print_status "Qdrant dashboard at: http://localhost:6333"
}

# Function to stop services
stop_services() {
    print_status "Stopping RAG system services..."
    docker-compose down
    print_success "Services stopped successfully"
}

# Function to show logs
show_logs() {
    print_status "Showing service logs..."
    docker-compose logs -f
}

# Function to show help
show_help() {
    echo "RAG Production System - Quick Setup Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  setup     - Complete setup and start services"
    echo "  start     - Start services"
    echo "  stop      - Stop services"
    echo "  logs      - Show service logs"
    echo "  status    - Show service status"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 setup     # Complete setup and start"
    echo "  $0 start     # Start services"
    echo "  $0 stop      # Stop services"
    echo "  $0 logs      # View logs"
}

# Function to show service status
show_status() {
    print_status "Service Status:"
    docker-compose ps
    
    echo ""
    print_status "Network Status:"
    docker network ls | grep rag
    
    echo ""
    print_status "Volume Status:"
    docker volume ls | grep rag
}

# Main script logic
main() {
    case "${1:-setup}" in
        "setup")
            print_status "Starting RAG Production System setup..."
            check_docker
            setup_env
            create_directories
            start_services
            ;;
        "start")
            start_services
            ;;
        "stop")
            stop_services
            ;;
        "logs")
            show_logs
            ;;
        "status")
            show_status
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Check if script is run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
