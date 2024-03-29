"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from datetime import timedelta


ALLOWED_HOSTS = [
    os.getenv('DEFAULT_HOST', 'web.com.ar'),
]

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'fake_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv('DEBUG', 'true') == 'true' else False

# If AWS is enabled, media will be stored in an S3 bucket
AWS_ENABLED = True if os.getenv('AWS_ENABLED', 'false') == 'true' else False

ADMINS = (
    ('Nahuel Fernandez', 'naha90@gmail.com'),
)


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.postgres',

    # Basic app
    'core',

    # Third-party apps
    'import_export',
    'solo',
    'celery',
]

if DEBUG:
    INSTALLED_APPS += ['rosetta']


# DATABASE
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': os.getenv('DB_NAME', 'db_name'),
       'USER': os.getenv('DB_USER', 'db_username'),
       'PASSWORD': os.getenv('DB_PASS', 'db_password'),
       'HOST': os.getenv('DB_SERVICE', 'localhost'),
       'PORT': os.getenv('DB_PORT', '5432'),
   }
}

# IMPORTANT - CUSTOM MODEL FOR USER
AUTH_USER_MODEL = 'core.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

GRAFANA_HOST = os.getenv('GRAFANA_HOST', '')
GRAFANA_API_KEY = os.getenv('GRAFANA_API_KEY', '')

WEB3_INFURA_POLYGON_URL = os.getenv('WEB3_INFURA_POLYGON_URL', '')
WEB3_INFURA_PROJECT_ID = os.getenv('WEB3_INFURA_PROJECT_ID', '')
WEB3_INFURA_API_SECRET = os.getenv('WEB3_INFURA_API_SECRET', '')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "backend/templates"), './templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

LANGUAGE_CODE = 'es'
LANGUAGES = (
    ('es', 'Español'),
)

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'

SITE_ID = 1
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
REDIS_DB = os.getenv('REDIS_DB', '0')

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ENABLE_UTC = True

from .celery_beat_schedule import beat_schedule
CELERY_BEAT_SCHEDULE = beat_schedule

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# EMAIL
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', True)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'web@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '--------')
EMAIL_FROM_ADDRESS = os.getenv('EMAIL_FROM_ADDRESS', 'web@gmail.com')

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Development server
if os.getenv('DEVSERVER', 'true') == 'true':
    ALLOWED_HOSTS.extend([
        'localhost:3000',
        'localhost:3001',
        'api.localhost',
        'localhost',
        '0.0.0.0'
    ])

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

RUN_ASYNC = os.getenv('RUN_ASYNC', 'True') == 'True'


