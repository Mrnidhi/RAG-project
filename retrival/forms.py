# =============================================================================
# RAG Production System - Form Definitions
# =============================================================================
# 
# This module defines Django forms for user input validation and
# data collection. It provides structured ways to handle PDF uploads
# and ensures data integrity through form validation.
# 
# Author: [Your Name]
# Project: RAG Production System
# Version: 1.0.0
# 
# Forms:
# - PDFUploadForm: Handles PDF file uploads with validation
# =============================================================================

from django import forms


class PDFUploadForm(forms.Form):
    """
    Django form for handling PDF file uploads.
    
    This form provides a structured way to collect PDF files from users
    and includes built-in validation to ensure only valid PDF documents
    are accepted. The form integrates with Django's file handling
    system for secure and efficient file processing.
    
    Attributes:
        pdf_file: FileField for capturing PDF uploads with validation
    """
    
    # File field for PDF uploads with comprehensive validation
    # required=True ensures users must provide a file before submission
    # The label provides clear user interface text
    pdf_file = forms.FileField(
        label="Upload PDF Document",
        required=True,
        help_text="Select a PDF file to upload for analysis and question answering",
        widget=forms.FileInput(attrs={
            'accept': '.pdf',  # Restrict file selection to PDFs only
            'class': 'form-control',  # Bootstrap styling class
            'id': 'pdf-upload-input'  # Unique identifier for JavaScript
        })
    )

    def clean_pdf_file(self):
        """
        Custom validation method for PDF file uploads.
        
        This method performs additional validation beyond Django's
        built-in file validation, ensuring the uploaded file meets
        specific requirements for the RAG system.
        
        Returns:
            UploadedFile: The validated PDF file
            
        Raises:
            forms.ValidationError: If the file doesn't meet requirements
        """
        uploaded_file = self.cleaned_data.get('pdf_file')
        
        if uploaded_file is None:
            raise forms.ValidationError("Please select a PDF file to upload.")
        
        # Validate file size (limit to 10MB for performance)
        if uploaded_file.size > 10 * 1024 * 1024:  # 10MB in bytes
            raise forms.ValidationError(
                "File size must be less than 10MB. Please choose a smaller PDF."
            )
        
        # Validate file extension
        if not uploaded_file.name.lower().endswith('.pdf'):
            raise forms.ValidationError(
                "Only PDF files are allowed. Please upload a valid PDF document."
            )
        
        return uploaded_file
