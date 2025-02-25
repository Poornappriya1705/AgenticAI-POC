import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, renderers, parsers
from .models import Document
from .serializers import DocumentUploadSerializer, ComplianceReportSerializer
from .utils import extract_text_from_pdf, extract_text_from_word
from .agents import check_compliance, modify_text

def report_to_table(report):
    """
    Convert a compliance report dictionary into an HTML table.
    """
    html = "<table border='1' style='border-collapse: collapse; width: 100%;'>"
    html += "<thead><tr><th style='padding: 5px;'>Metric</th><th style='padding: 5px;'>Result</th></tr></thead>"
    html += "<tbody>"
    for key, value in report.items():
        html += f"<tr><td style='padding: 5px;'>{key.capitalize()}</td><td style='padding: 5px;'>{value}</td></tr>"
    html += "</tbody></table>"
    return html

class DocumentUploadAndComplianceView(APIView):
    """
    Endpoint to upload a document and immediately check compliance.
    Returns the compliance report (HTML table) along with document info.
    """
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    renderer_classes = [renderers.JSONRenderer, renderers.TemplateHTMLRenderer]

    def post(self, request, *args, **kwargs):
        serializer = DocumentUploadSerializer(data=request.data)
        if serializer.is_valid():
            document = serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Process file for compliance
        file_path = os.path.join(settings.MEDIA_ROOT, document.file.name)
        ext = document.file.name.split('.')[-1].lower()
        if ext == "pdf":
            text = extract_text_from_pdf(file_path)
        elif ext in ["doc", "docx"]:
            text = extract_text_from_word(file_path)
        else:
            return Response({"error": "Unsupported file type."}, status=status.HTTP_400_BAD_REQUEST)
        
        compliance_report = check_compliance(text)
        compliance_table = report_to_table(compliance_report)
        response_data = {
            "document_id": document.id,
            "compliance_report_table": compliance_table,
            "file_url": document.file.url
        }
        return Response(response_data, status=status.HTTP_200_OK)

class DocumentComplianceView(APIView):
    """
    Endpoint to check compliance for an already uploaded document.
    This view is used by the UI (via a GET request) to display the compliance report.
    """
    renderer_classes = [renderers.JSONRenderer, renderers.TemplateHTMLRenderer]
    parser_classes = [parsers.JSONParser, parsers.FormParser]

    def get(self, request, document_id, *args, **kwargs):
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            return Response({"error": "Document not found."}, status=status.HTTP_404_NOT_FOUND)
        file_path = os.path.join(settings.MEDIA_ROOT, document.file.name)
        ext = document.file.name.split('.')[-1].lower()
        if ext == "pdf":
            text = extract_text_from_pdf(file_path)
        elif ext in ["doc", "docx"]:
            text = extract_text_from_word(file_path)
        else:
            return Response({"error": "Unsupported file type."}, status=status.HTTP_400_BAD_REQUEST)
        compliance_report = check_compliance(text)
        compliance_table = report_to_table(compliance_report)
        response_data = {"document_id": document.id, "compliance_report_table": compliance_table}
        return Response(response_data, status=status.HTTP_200_OK)

class DocumentModifyView(APIView):
    """
    Endpoint to modify the document text based on the compliance report.
    Returns the modified text and a download link.
    """
    renderer_classes = [renderers.JSONRenderer, renderers.TemplateHTMLRenderer]
    parser_classes = [parsers.JSONParser, parsers.FormParser]

    def post(self, request, document_id, *args, **kwargs):
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            return Response({"error": "Document not found."}, status=status.HTTP_404_NOT_FOUND)
        
        file_path = os.path.join(settings.MEDIA_ROOT, document.file.name)
        ext = document.file.name.split('.')[-1].lower()
        if ext == "pdf":
            text = extract_text_from_pdf(file_path)
        elif ext in ["doc", "docx"]:
            text = extract_text_from_word(file_path)
        else:
            return Response({"error": "Unsupported file type."}, status=status.HTTP_400_BAD_REQUEST)
        
        modified_text = modify_text(text)
        # Combine original text with modifications.
        combined_text = text + "\n\n--- Compliance Changes Applied ---\n\n" + modified_text
        
        # Save the combined text to a new file.
        base, _ = os.path.splitext(file_path)
        modified_file_path = f"{base}_modified.txt"  # Save as a text file for simplicity.
        with open(modified_file_path, "w", encoding="utf-8") as f:
            f.write(combined_text)
        
        download_url = request.build_absolute_uri(
            settings.MEDIA_URL + os.path.basename(modified_file_path)
        )
        response_data = {
            "document_id": document.id,
            "modified_text": combined_text,
            "modified_file_url": download_url
        }
        return Response(response_data, status=status.HTTP_200_OK)
        # base, _ = os.path.splitext(file_path)
        # modified_file_path = f"{base}_modified.{ext}"
        # with open(modified_file_path, "w", encoding="utf-8") as f:
        #     f.write(modified_text)
        
        # download_url = request.build_absolute_uri(settings.MEDIA_URL + os.path.basename(modified_file_path))
        # response_data = {
        #     "document_id": document.id,
        #     "modified_text": modified_text,
        #     "modified_file_url": download_url
        # }
        # return Response(response_data, status=status.HTTP_200_OK)

# Simple view to render the single-page UI.
from django.shortcuts import render
def api_test_view(request):
    return render(request, "document_analysis/api_test.html")
