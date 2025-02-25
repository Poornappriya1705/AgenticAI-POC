import os
from pathlib import Path
import django.core.wsgi
###  Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your_secret_key' # Replace with your secret

DEBUG = True

ALLOWED_HOSTS =['agenticai-poc.onrender.com']

## application definiton
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'document_analysis',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'ai_document_compliance.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':[os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS':{
            'context_processors':[
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ai_document_compliance.wsgi.application'

## Database (using sqlite3 for simplicity)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR/'db.sqlite3',
    }
}

### Password Validation (default)
AUTH_PASSWORDS_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':'django.contrib.auth.password_valiation.MinimumLengthValidator',
    },
    {
        'NAME':'django.contrib.auth.password_valiation.CommonPasswordValidator',
    },
    {
        'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'
    },
]


### Defining the Time Zone
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

## Static Path
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'document_analysis/static')
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

## Media Configuration for file upload
MEDIA_URL = '/media/'
MEDIA_PORT = os.path.join(BASE_DIR,'documents')

### Django Rest Framework Setting (Optional)
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSESS':[
        'rest_framework.permissions.AllowAny',
    ]
}