# =============================================================================
# RAG Production System - Test Suite
# =============================================================================
# 
# This module contains comprehensive test cases for the retrieval
# application, ensuring that all functionality works correctly
# and maintains quality standards across development iterations.
# 
# Author: [Your Name]
# Project: RAG Production System
# Version: 1.0.0
# 
# Test Coverage:
# - Model validation and relationships
# - View function behavior
# - Form validation and processing
# - URL routing and navigation
# - Admin interface functionality
# =============================================================================

from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from .models import UploadedPDF, Query
from .forms import PDFUploadForm


class UploadedPDFModelTest(TestCase):
    """
    Test cases for the UploadedPDF model.
    
    This test class validates the behavior of the UploadedPDF model,
    including field validation, string representation, and metadata
    handling for uploaded PDF documents.
    """
    
    def setUp(self):
        """
        Set up test data for each test method.
        
        This method runs before each test, creating a clean
        environment and sample data for testing purposes.
        """
        # Create a sample PDF file for testing
        self.sample_pdf = SimpleUploadedFile(
            "test_document.pdf",
            b"PDF content for testing purposes",
            content_type="application/pdf"
        )
    
    def test_uploaded_pdf_creation(self):
        """
        Test that UploadedPDF instances can be created successfully.
        
        This test verifies that the model can store PDF files
        with proper metadata and timestamps.
        """
        pdf = UploadedPDF.objects.create(
            file=self.sample_pdf,
            name="Test PDF Document"
        )
        
        # Verify the PDF was created with correct attributes
        self.assertEqual(pdf.name, "Test PDF Document")
        self.assertIsNotNone(pdf.uploaded_at)
        self.assertEqual(pdf.file.name, "uploads/test_document.pdf")
    
    def test_uploaded_pdf_string_representation(self):
        """
        Test the string representation of UploadedPDF instances.
        
        This test ensures that the __str__ method returns
        meaningful information for display purposes.
        """
        # Test with custom name
        pdf_with_name = UploadedPDF.objects.create(
            file=self.sample_pdf,
            name="Custom Named PDF"
        )
        self.assertEqual(str(pdf_with_name), "Custom Named PDF")
        
        # Test without custom name (should use timestamp)
        pdf_without_name = UploadedPDF.objects.create(file=self.sample_pdf)
        self.assertIn("PDF uploaded at", str(pdf_without_name))


class QueryModelTest(TestCase):
    """
    Test cases for the Query model.
    
    This test class validates the behavior of the Query model,
    including relationships with UploadedPDF and response handling.
    """
    
    def setUp(self):
        """
        Set up test data for each test method.
        
        Creates sample PDF and query data for testing
        the Query model functionality.
        """
        # Create a sample PDF for testing
        self.sample_pdf = SimpleUploadedFile(
            "test_document.pdf",
            b"PDF content for testing",
            content_type="application/pdf"
        )
        self.pdf = UploadedPDF.objects.create(
            file=self.sample_pdf,
            name="Test PDF"
        )
    
    def test_query_creation(self):
        """
        Test that Query instances can be created successfully.
        
        Verifies that queries can be associated with PDFs
        and store both questions and responses.
        """
        query = Query.objects.create(
            user_query="What is this document about?",
            response="This is a test document for testing purposes.",
            pdf=self.pdf
        )
        
        # Verify the query was created correctly
        self.assertEqual(query.user_query, "What is this document about?")
        self.assertEqual(query.response, "This is a test document for testing purposes.")
        self.assertEqual(query.pdf, self.pdf)
        self.assertIsNotNone(query.created_at)
    
    def test_query_pdf_relationship(self):
        """
        Test the relationship between Query and UploadedPDF models.
        
        Ensures that queries are properly linked to their
        corresponding PDF documents.
        """
        query = Query.objects.create(
            user_query="Test question",
            pdf=self.pdf
        )
        
        # Verify the relationship works in both directions
        self.assertEqual(query.pdf, self.pdf)
        self.assertIn(query, self.pdf.queries.all())


class PDFUploadFormTest(TestCase):
    """
    Test cases for the PDFUploadForm.
    
    This test class validates form validation, file handling,
    and user input processing for PDF uploads.
    """
    
    def test_valid_pdf_upload(self):
        """
        Test that valid PDF files are accepted by the form.
        
        Verifies that the form correctly processes
        properly formatted PDF documents.
        """
        pdf_file = SimpleUploadedFile(
            "valid_document.pdf",
            b"Valid PDF content",
            content_type="application/pdf"
        )
        
        form_data = {}
        file_data = {'pdf_file': pdf_file}
        form = PDFUploadForm(data=form_data, files=file_data)
        
        self.assertTrue(form.is_valid())
    
    def test_invalid_file_type(self):
        """
        Test that non-PDF files are rejected by the form.
        
        Ensures that only PDF documents are accepted
        to maintain system integrity.
        """
        text_file = SimpleUploadedFile(
            "document.txt",
            b"Text content, not PDF",
            content_type="text/plain"
        )
        
        form_data = {}
        file_data = {'pdf_file': text_file}
        form = PDFUploadForm(data=form_data, files=file_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('pdf_file', form.errors)


class ViewFunctionTest(TestCase):
    """
    Test cases for view functions.
    
    This test class validates the behavior of view functions,
    including request handling, response generation, and
    template rendering.
    """
    
    def setUp(self):
        """
        Set up test client and data for view testing.
        
        Initializes the Django test client and creates
        sample data for testing view functions.
        """
        self.client = Client()
        self.sample_pdf = SimpleUploadedFile(
            "test_document.pdf",
            b"PDF content for testing",
            content_type="application/pdf"
        )
    
    def test_upload_page_access(self):
        """
        Test that the upload page is accessible.
        
        Verifies that users can access the PDF upload
        interface without authentication requirements.
        """
        response = self.client.get(reverse('upload_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload.html')
    
    def test_ask_question_page_access(self):
        """
        Test that the question page is accessible.
        
        Verifies that users can access the question
        answering interface.
        """
        response = self.client.get(reverse('ask_question'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ask_question.html')


class AdminInterfaceTest(TestCase):
    """
    Test cases for the Django admin interface.
    
    This test class validates that the admin interface
    is properly configured and functional.
    """
    
    def setUp(self):
        """
        Set up admin user and test data.
        
        Creates a superuser account and sample data
        for testing admin functionality.
        """
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.client = Client()
        self.client.login(username='admin', password='adminpass123')
    
    def test_admin_uploaded_pdf_access(self):
        """
        Test that admin can access UploadedPDF admin interface.
        
        Verifies that the admin interface for PDF documents
        is properly configured and accessible.
        """
        response = self.client.get('/admin/retrival/uploadedpdf/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_query_access(self):
        """
        Test that admin can access Query admin interface.
        
        Verifies that the admin interface for queries
        is properly configured and accessible.
        """
        response = self.client.get('/admin/retrival/query/')
        self.assertEqual(response.status_code, 200)
