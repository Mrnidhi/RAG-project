# =============================================================================
# RAG Production System - Docker Configuration
# =============================================================================
# 
# This Dockerfile creates a production-ready container for the
# Retrieval-Augmented Generation (RAG) application. It sets up a
# Python environment with all necessary dependencies and configurations
# for running the Django application in a containerized environment.
# 
# Author: [Your Name]
# Project: RAG Production System
# Version: 1.0.0
# 
# Build Command: docker build -t rag-app .
# Run Command: docker run -p 8000:8000 rag-app
# =============================================================================

# Use official Python 3.12 slim image as base for optimal size and security
FROM python:3.12-slim

# Set environment variables for Python optimization and security
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies required for building Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        && rm -rf /var/lib/apt/lists/*

# Set the working directory for the application
WORKDIR /app

# Copy requirements file first for better Docker layer caching
COPY requirements.txt /app/

# Install Python dependencies with optimized pip settings
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire application codebase to the container
COPY . /app/

# Expose port 8000 for the Django application
EXPOSE 8000

# Start the production server using Gunicorn with custom configuration
# The custom config provides optimized worker settings and timeout configurations
CMD ["gunicorn", "rag.wsgi:application", "--config", "gunicorn.conf.py"]
