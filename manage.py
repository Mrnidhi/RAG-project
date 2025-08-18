#!/usr/bin/env python
"""
Django Management Script for RAG Production System

This script serves as the command-line utility for administrative tasks
in the Retrieval-Augmented Generation (RAG) application. It provides
access to Django's management commands for database operations,
development server management, and administrative functions.

Author: [Your Name]
Project: RAG Production System
Version: 1.0.0
"""

import os
import sys


def main():
    """
    Main entry point for Django management commands.
    
    This function initializes the Django environment and executes
    the specified management command. It sets up the necessary
    environment variables and Django settings before running commands.
    """
    # Set the Django settings module for the application
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rag.settings')
    
    try:
        # Import Django's management utilities
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Handle import errors gracefully with informative messages
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Execute the management command with provided arguments
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
