# =============================================================================
# RAG Production System - Django Settings Configuration
# =============================================================================
# 
# This file contains all Django framework settings for the
# Retrieval-Augmented Generation (RAG) application. It configures
# database connections, security settings, middleware, and application
# behavior for both development and production environments.
# 
# Author: [Your Name]
# Project: RAG Production System
# Version: 1.0.0
# 
# For more information on Django settings, see:
# https://docs.djangoproject.com/en/5.2/topics/settings/
# =============================================================================

from pathlib import Path

# =============================================================================
# PROJECT PATH CONFIGURATION
# =============================================================================
# Build paths inside the project using BASE_DIR / 'subdir'
# This provides a reliable way to reference project directories
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# SECURITY CONFIGURATION
# =============================================================================
# SECURITY WARNING: Keep the secret key used in production secret!
# This key is used for cryptographic signing and should be unique
SECRET_KEY = 'django-insecure-tipb=uv)c96-8n*fm*7s8q=g*=7f+st7&g==_sl#2s6kw(*9rg'

# SECURITY WARNING: Don't run with debug turned on in production!
# Debug mode provides detailed error pages but exposes sensitive information
DEBUG = True

# List of host/domain names that this Django site can serve
# Add your production domain names here when deploying
ALLOWED_HOSTS = ['15.207.20.199', 'localhost', '127.0.0.1']

# =============================================================================
# APPLICATION DEFINITION
# =============================================================================
# Django applications that are enabled in this Django instance
INSTALLED_APPS = [
    # Django built-in applications for core functionality
    'django.contrib.admin',          # Admin interface
    'django.contrib.auth',           # Authentication system
    'django.contrib.contenttypes',   # Content type framework
    'django.contrib.sessions',       # Session framework
    'django.contrib.messages',       # Messaging framework
    'django.contrib.staticfiles',    # Static file management
    
    # Custom application for RAG functionality
    'retrival',                      # PDF uploads and vector search operations
]

# =============================================================================
# MIDDLEWARE CONFIGURATION
# =============================================================================
# Middleware classes that process requests and responses
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',        # Security enhancements
    'django.contrib.sessions.middleware.SessionMiddleware', # Session management
    'django.middleware.common.CommonMiddleware',            # Common functionality
    'django.middleware.csrf.CsrfViewMiddleware',            # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware', # User authentication
    'django.contrib.messages.middleware.MessageMiddleware', # Message framework
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Clickjacking protection
]

# =============================================================================
# URL CONFIGURATION
# =============================================================================
# Root URL configuration for the Django project
ROOT_URLCONF = 'rag.urls'

# =============================================================================
# TEMPLATE CONFIGURATION
# =============================================================================
# Template engine settings for rendering HTML pages
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Additional template directories
        'APP_DIRS': True,  # Look for templates in app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',      # Debug context
                'django.template.context_processors.request',    # Request context
                'django.contrib.auth.context_processors.auth',  # User context
                'django.contrib.messages.context_processors.messages', # Messages context
            ],
        },
    },
]

# =============================================================================
# WSGI APPLICATION CONFIGURATION
# =============================================================================
# WSGI application entry point for production deployment
WSGI_APPLICATION = 'rag.wsgi.application'

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
# Database settings for storing application data
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # SQLite database engine
        'NAME': BASE_DIR / 'db.sqlite3',         # Database file location
    }
}

# =============================================================================
# PASSWORD VALIDATION
# =============================================================================
# Password validation rules for user authentication
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# =============================================================================
# INTERNATIONALIZATION
# =============================================================================
# Language and timezone settings for internationalization
LANGUAGE_CODE = 'en-us'  # Default language for the application
TIME_ZONE = 'UTC'        # Default timezone for datetime operations
USE_I18N = True          # Enable internationalization
USE_TZ = True            # Enable timezone support

# =============================================================================
# STATIC FILES CONFIGURATION
# =============================================================================
# Settings for serving static files (CSS, JavaScript, images)
STATIC_URL = 'static/'                    # URL prefix for static files
STATIC_ROOT = BASE_DIR / "staticfiles"    # Directory for collected static files

# =============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# =============================================================================
# Default field type for primary keys in models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
