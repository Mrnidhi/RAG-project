# =============================================================================
# RAG Production System - WSGI Application Configuration
# =============================================================================
# 
# This file configures the WSGI (Web Server Gateway Interface) application
# for the RAG system. WSGI is a specification that allows web servers
# to communicate with Python web applications, enabling deployment
# in production environments with servers like Gunicorn or uWSGI.
# 
# Author: [Your Name]
# Project: RAG Production System
# Version: 1.0.0
# 
# For more information on WSGI deployment, see:
# https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
# =============================================================================

import os

# Import Django's WSGI application factory function
from django.core.wsgi import get_wsgi_application

# Set the Django settings module for the WSGI application
# This tells Django which settings file to use for configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rag.settings')

# Create the WSGI application object
# This is the callable object that web servers will use to handle requests
application = get_wsgi_application()
