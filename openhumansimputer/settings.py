"""
Django settings for openhumansimputer project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import dj_database_url
from env_tools import apply_env
import logging
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

logger = logging.getLogger(__name__)

apply_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if os.getenv('DEBUG', '').lower() == 'false' else True

print('DEBUG: {}'.format(DEBUG))

REMOTE = True if os.getenv('REMOTE', '').lower() == 'true' else False
print('REMOTE: {}'.format(REMOTE))

#ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ['.openimpute.com', '68.65.121.62']

REMOTE_APP_NAME = os.getenv('REMOTE_APP_NAME', '')
DEFAULT_BASE_URL = ('http://{}'.format(REMOTE_APP_NAME) if
                    REMOTE else 'http://127.0.0.1:5000')

#HEROKUCONFIG_APP_NAME = 'http://142.93.20.214'
#DEFAULT_BASE_URL = 'http://142.93.20.214:8000'

OPENHUMANS_APP_BASE_URL = os.getenv('APP_BASE_URL', DEFAULT_BASE_URL)
if OPENHUMANS_APP_BASE_URL[-1] == "/":
    OPENHUMANS_APP_BASE_URL = OPENHUMANS_APP_BASE_URL[:-1]

OPENHUMANS_APP_REDIRECT_URI = OPENHUMANS_APP_BASE_URL + '/complete'

# Open Humans configuration
OPENHUMANS_CLIENT_ID = os.getenv('OH_CLIENT_ID')
OPENHUMANS_CLIENT_SECRET = os.getenv('OH_CLIENT_SECRET')
OH_ACTIVITY_PAGE = os.getenv('OH_ACTIVITY_PAGE')
OPENHUMANS_OH_BASE_URL = 'https://www.openhumans.org'

OH_API_BASE = OPENHUMANS_OH_BASE_URL + '/api/direct-sharing'
OH_DIRECT_UPLOAD = OH_API_BASE + '/project/files/upload/direct/'
OH_DIRECT_UPLOAD_COMPLETE = OH_API_BASE + '/project/files/upload/complete/'
OH_DELETE_FILES = OH_API_BASE + '/project/files/delete/'

# Imputer Settings
# in production this should be False
TEST_CHROMS = True if os.environ.get(
    'TEST_CHROMS', '').lower() == 'true' else False
if TEST_CHROMS:
    print('using chr21 and chr22 for testing')
    CHROMOSOMES = ["{}".format(i)
                   for i in list(range(5, 8))]  + ["23"]
else:
    CHROMOSOMES = ["{}".format(i)
                   for i in list(range(1, 24))]

# Applications installed
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps. Update these if you add or change app names!
    'imputer.apps.ImputerConfig',
    'datauploader.apps.DatauploaderConfig',
    'open_humans.apps.OpenHumansConfig',
    'main.apps.MainConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

MIDDLEWARE_CLASSES = (
    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    'whitenoise.middleware.WhiteNoiseMiddleware'
)

ROOT_URLCONF = 'openhumansimputer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'openhumansimputer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
# https://devcenter.heroku.com/articles/django-app-configuration


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'UserAttributeSimilarityValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'MinimumLengthValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'CommonPasswordValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'NumericPasswordValidator'),
    },
]


# Configure logging.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'gunicorn': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': '/home/kevin/logs//gunicorn.errors',
            'maxBytes': 1024 * 1024 * 200,  # 100 mb
        },
	'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'gunicorn.errors': {
            'level': 'DEBUG',
            'handlers': ['gunicorn'],
            'propagate': True,
        },
	'oh': {
		'level': 'DEBUG',
		'handlers': ['console'],
		'propogate': True
    }
}
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

INSTALLED_APPS += ['django_extensions']

# celery settings
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
# Directory config, change these if you have a different setup.
# Also make sure these are in /etc/default/celeryd
IMP_BIN='/home/kevin/impbin'
REF_PANEL='/home/kevin/1000GP_Phase3'
DATA_DIR='/home/kevin/data'
REF_FA='/home/kevin/hg19'
OUT_DIR='/home/kevin/outdir'

# Sentry
sentry_sdk.init(
    dsn="https://113d97f46e91488b91cc664e94a9d8e2@sentry.io/1294965",
    integrations=[DjangoIntegration(), CeleryIntegration()]
)
