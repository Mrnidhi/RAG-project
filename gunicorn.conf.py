# =============================================================================
# RAG Production System - Gunicorn Configuration
# =============================================================================
# 
# This configuration file optimizes Gunicorn settings for production
# deployment of the RAG application. It includes worker management,
# timeout configurations, and logging settings tailored for high
# performance and stability in production environments.
# 
# Author: [Your Name]
# Project: RAG Production System
# Version: 1.0.0
# 
# Usage: gunicorn rag.wsgi:application --config gunicorn.conf.py
# =============================================================================

import multiprocessing

# =============================================================================
# SERVER SOCKET CONFIGURATION
# =============================================================================
# Bind the server to all available network interfaces on port 8000
bind = "0.0.0.0:8000"
# Maximum number of pending connections in the queue
backlog = 2048

# =============================================================================
# WORKER PROCESS CONFIGURATION
# =============================================================================
# Calculate optimal number of workers based on CPU cores
# Formula: (2 x num_cores) + 1 for optimal performance
workers = multiprocessing.cpu_count() * 2 + 1
# Use synchronous workers for Django compatibility
worker_class = "sync"
# Maximum number of simultaneous connections per worker
worker_connections = 1000
# Restart workers after handling this many requests to prevent memory leaks
max_requests = 1000
# Add randomness to worker restarts to prevent all workers restarting simultaneously
max_requests_jitter = 50
# Preload application code to improve startup time
preload_app = True

# =============================================================================
# TIMEOUT AND CONNECTION SETTINGS
# =============================================================================
# Maximum time (seconds) a worker can spend processing a single request
timeout = 120  # Increased from default 30 seconds for RAG operations
# Time to wait for the next request on a keep-alive connection
keepalive = 2
# Time to wait for workers to finish processing requests before shutdown
graceful_timeout = 30

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================
# Log access requests to stdout for container logging
accesslog = "-"
# Log errors to stdout for container logging
errorlog = "-"
# Set logging level for detailed debugging information
loglevel = "info"
# Custom format for access logs with additional request details
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# =============================================================================
# PROCESS NAMING AND IDENTIFICATION
# =============================================================================
# Name for the main process in system monitoring tools
proc_name = "rag-app"

# =============================================================================
# SERVER MECHANICS AND SECURITY
# =============================================================================
# Run in foreground mode (not as a daemon) for container environments
daemon = False
# No PID file needed for containerized deployment
pidfile = None
# Set file creation mask for security
umask = 0
# Run as root user (default for containers)
user = None
# Run as root group (default for containers)
group = None
# No temporary upload directory needed
tmp_upload_dir = None

# =============================================================================
# SSL CONFIGURATION (COMMENTED OUT FOR HTTP DEPLOYMENT)
# =============================================================================
# Uncomment and configure these lines for HTTPS deployment
# keyfile = None
# certfile = None
