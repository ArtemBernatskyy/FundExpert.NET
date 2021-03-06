"""
Django settings for mutual_funds project.

Generated by 'django-admin startproject' using Django 1.9.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(__file__)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret_here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'grappelli.dashboard',
    'grappelli',
    'django.contrib.admin',
    'mutual_funds.registration',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # debug
    # 'debug_toolbar',
    # 'debug_panel',
    'django.contrib.sites',
    # third party apps
    'django_countries',
    'djcelery_email',
    'rest_framework',
    'memoize',
    'ckeditor',
    'imagekit',
    'bootstrap3',
    'captcha',
    'django_select2',
    'widget_tweaks',
    # local apps
    'mutual_funds.finance',
    'mutual_funds.landing',
    'mutual_funds.accounts',
    'mutual_funds.company',
]

SITE_ID = 1

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',    # classic debug
    # 'debug_panel.middleware.DebugPanelMiddleware',        # api based debug + classic + chromeext
    'async_messages.middleware.AsyncMiddleware',
]

ROOT_URLCONF = 'mutual_funds.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'mutual_funds.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_name',
        'USER': 'user_name',
        'PASSWORD': 'somepass',
        'HOST': '127.0.0.1',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en', 'English'),
    ('ru', 'Русский'),
)

# Translations
LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/var/webapps/mutual_funds/www/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# select2 Set the cache backend to select2
SELECT2_CACHE_BACKEND = 'default'

# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/webapps/mutual_funds/www/media/'

# Grapelli Admin Theme
GRAPPELLI_ADMIN_TITLE = 'FundExpert Project'
GRAPPELLI_INDEX_DASHBOARD = 'mutual_funds.dashboard.CustomIndexDashboard'

# CKeditor
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None
    }
}

# Registration Redux
ACCOUNT_ACTIVATION_DAYS = 1
REGISTRATION_EMAIL_HTML = True
REGISTRATION_AUTO_LOGIN = True
LOGIN_REDIRECT_URL = "landing:main_page"

# Recaptcha
RECAPTCHA_PUBLIC_KEY = 'somekey'
RECAPTCHA_PRIVATE_KEY = 'other-key'
RECAPTCHA_USE_SSL = True
NOCAPTCHA = True

# Email
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'lol.com@gmail.com'
EMAIL_HOST_PASSWORD = 'lolpass'
EMAIL_PORT = 587

# Django countries
COUNTRIES_FIRST = ['RU', 'KZ', 'BY', 'UA']

# Django money
CURRENCIES = ('USD', 'EUR')

# CELERY SETTINGS
BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Trustnet access
TRUSTNET_USERNAME = "othermail@gmail.com"
TRUSTNET_PASSWORD = "otherpass"

# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}


# # Debug-Toolbar conf
# INTERNAL_IPS = ('172.16.0.59', '127.0.0.1', '0.0.0.0', '10.0.2.15', '10.0.2.2')
# # Be careful it will show toolbar forany IP
# def show_toolbar(request):
#     return True
# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TOOLBAR_CALLBACK': 'mutual_funds.settings.show_toolbar',
# }

# Celery Email
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
