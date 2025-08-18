# =============================================================================
# RAG Production System - Retrieval Application URL Configuration
# =============================================================================
# 
# This module defines the URL routing for the retrieval application.
# It maps specific URL patterns to view functions that handle
# HTTP requests for PDF uploads and question answering functionality.
# 
# Author: [Your Name]
# Project: RAG Production System
# Version: 1.0.0
# 
# URL Patterns:
# - /upload/: PDF document upload interface
# - /ask/: Question answering interface for uploaded documents
# =============================================================================

from django.urls import path
from . import views

# =============================================================================
# URL PATTERN DEFINITIONS
# =============================================================================
# Define the URL patterns that map to specific view functions
# Each path() function creates a URL route with a descriptive name
urlpatterns = [
    # PDF Upload Endpoint
    # This route handles the interface for users to upload PDF documents
    # The view function processes the uploaded file and stores it for analysis
    path('upload/', views.upload_pdf, name='upload_pdf'),
    
    # Question Answering Endpoint
    # This route provides the interface for users to ask questions about
    # uploaded PDF documents and receive AI-generated responses
    path('ask/', views.ask_question, name='ask_question'),
]