from django.urls import path
from .views import (
    DocumentUploadAndComplianceView,
    DocumentComplianceView,
    DocumentModifyView,
    api_test_view
)

urlpatterns = [
    path('upload/', DocumentUploadAndComplianceView.as_view(), name='document-upload'),
    path('compliance/<int:document_id>/', DocumentComplianceView.as_view(), name='document-compliance'),
    path('modify/<int:document_id>/', DocumentModifyView.as_view(), name='document-modify'),
    path('test/', api_test_view, name='api-test'),
]
