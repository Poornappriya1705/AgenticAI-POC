import os
import django.core.wsgi 
from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE","ai_document_compliance.settings")

application = get_wsgi_application()