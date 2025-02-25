from rest_framework import serializers
from .models import Document

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'file', 'uploaded_at']

    def validate_file(self, value):
        allowed_extensions = ['pdf', 'doc', 'docx']
        ext = value.name.split('.')[-1].lower()
        if ext not in allowed_extensions:
            raise serializers.ValidationError("Unsupported file extension.")
        return value

class ComplianceReportSerializer(serializers.Serializer):
    document_id = serializers.IntegerField()
    compliance_report = serializers.DictField()
    modified_text = serializers.CharField(required=False)
    modified_file_url = serializers.CharField(required=False)