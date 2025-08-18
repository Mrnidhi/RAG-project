# =============================================================================
# RAG Production System - Django Admin Interface Configuration
# =============================================================================
# 
# This module configures the Django admin interface for the retrieval
# application, providing administrators with a user-friendly way to
# manage uploaded PDFs, user queries, and system data through the
# web interface.
# 
# Author: [Your Name]
# Project: RAG Production System
# Version: 1.0.0
# 
# Admin Features:
# - PDF Document Management
# - Query and Response Tracking
# - User Activity Monitoring
# - System Data Administration
# =============================================================================

from django.contrib import admin
from .models import UploadedPDF, Query


@admin.register(UploadedPDF)
class UploadedPDFAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the UploadedPDF model.
    
    This class customizes how PDF documents are displayed and managed
    in the Django admin interface, providing administrators with
    comprehensive tools for document oversight and management.
    """
    
    # Fields to display in the admin list view
    list_display = ('name', 'uploaded_at', 'file', 'get_file_size')
    
    # Fields that can be used for filtering the admin list
    list_filter = ('uploaded_at',)
    
    # Fields that can be searched in the admin interface
    search_fields = ('name', 'file')
    
    # Fields that are read-only in the admin interface
    readonly_fields = ('uploaded_at',)
    
    # Fields to display in the admin detail view
    fieldsets = (
        ('Document Information', {
            'fields': ('name', 'file')
        }),
        ('Upload Details', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_file_size(self, obj):
        """
        Calculate and display the file size in human-readable format.
        
        Args:
            obj: The UploadedPDF instance
            
        Returns:
            str: Human-readable file size (e.g., "2.5 MB")
        """
        if obj.file and hasattr(obj.file, 'size'):
            size_bytes = obj.file.size
            # Convert bytes to human-readable format
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size_bytes < 1024.0:
                    return f"{size_bytes:.1f} {unit}"
                size_bytes /= 1024.0
            return f"{size_bytes:.1f} TB"
        return "Unknown"
    
    get_file_size.short_description = "File Size"
    get_file_size.admin_order_field = 'file'


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Query model.
    
    This class customizes how user queries and AI responses are displayed
    and managed in the Django admin interface, enabling administrators
    to monitor user interactions and system performance.
    """
    
    # Fields to display in the admin list view
    list_display = ('user_query', 'pdf', 'created_at', 'has_response')
    
    # Fields that can be used for filtering the admin list
    list_filter = ('created_at', 'pdf')
    
    # Fields that can be searched in the admin interface
    search_fields = ('user_query', 'response', 'pdf__name')
    
    # Fields that are read-only in the admin interface
    readonly_fields = ('created_at',)
    
    # Fields to display in the admin detail view
    fieldsets = (
        ('Query Information', {
            'fields': ('user_query', 'pdf')
        }),
        ('Response Data', {
            'fields': ('response',),
            'classes': ('collapse',)
        }),
        ('Timing Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def has_response(self, obj):
        """
        Check if the query has a generated response.
        
        Args:
            obj: The Query instance
            
        Returns:
            bool: True if response exists, False otherwise
        """
        return bool(obj.response and obj.response.strip())
    
    has_response.boolean = True
    has_response.short_description = "Has Response"
