# =============================================================================
# RAG Production System - Main URL Configuration
# =============================================================================
# 
# This file defines the main URL routing for the RAG application.
# It maps URL patterns to view functions and handles the overall
# navigation structure of the web application.
# 
# Author: [Your Name]
# Project: RAG Production System
# Version: 1.0.0
# 
# For more information on Django URL patterns, see:
# https://docs.djangoproject.com/en/5.2/topics/http/urls/
# =============================================================================

from django.contrib import admin
from django.urls import path, include
from retrival import views

# =============================================================================
# URL PATTERN DEFINITIONS
# =============================================================================
# Define the URL patterns that map to specific view functions
# Each path() function creates a URL route with a name for reverse lookup
urlpatterns = [
    # Root URL - Redirects users to the PDF upload page
    path('', views.redirect_to_upload, name='home_redirect'),
    
    # PDF Upload Page - Allows users to upload PDF documents for processing
    path('upload/', views.upload_pdf, name='upload_pdf'),
    
    # Question Answering Page - Enables users to ask questions about uploaded PDFs
    path('ask/', views.ask_question, name='ask_question'),
]

# =============================================================================
# URL PATTERN EXAMPLES (FOR REFERENCE)
# =============================================================================
# Function-based views:
#     1. Import the view: from my_app import views
#     2. Add URL pattern: path('', views.home, name='home')
# 
# Class-based views:
#     1. Import the view: from other_app.views import Home
#     2. Add URL pattern: path('', Home.as_view(), name='home')
# 
# Including other URL configurations:
#     1. Import include function: from django.urls import include, path
#     2. Add URL pattern: path('blog/', include('blog.urls'))
