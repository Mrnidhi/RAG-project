# =============================================================================
# RAG Production System - ASGI Application Configuration
# =============================================================================
# 
# This file configures the ASGI (Asynchronous Server Gateway Interface)
# application for the RAG system. ASGI is the modern successor to WSGI,
# enabling asynchronous web applications and real-time features like
# WebSockets for future enhancements.
# 
# Author: [Your Name]
# Project: RAG Production System
# Version: 1.0.0
# 
# For more information on ASGI deployment, see:
# https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
# =============================================================================

import os

# Import Django's ASGI application factory function
from django.core.asgi import get_asgi_application

# Set the Django settings module for the ASGI application
# This tells Django which settings file to use for configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rag.settings')

# Create the ASGI application object
# This is the callable object that ASGI servers will use to handle requests
application = get_asgi_application()
