import os
from pathlib import Path

CSRF_TRUSTED_ORIGINS = [
    'https://saes5.onrender.com',
]

AUTH_USER_MODEL = 'auth.User'
LOGIN_REDIRECT_URL = '/home/'
# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-gb6$j!l#(iokk_x+8yq@mo46%g@dai)s+w&2&f%hyk(vrwjmam')

DEBUG = True
# Allowed Hosts
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'saes5.onrender.com']
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    'INTERCEPT_REDIRECTS)': False,
}

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mousey',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',
    'debug_toolbar',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',

]

if DEBUG:
    INTERNAL_IPS = [
        '127.0.0.1',
        'localhost',
        '::1',  # IPv6
    ]


# URL Configuration
ROOT_URLCONF = 'mickey.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# WSGI application
WSGI_APPLICATION = 'mickey.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'cybermouse_db'),
        'USER': os.environ.get('DB_USER', '384089'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'A(h0U1ch0U!'),
        'HOST': os.environ.get('DB_HOST', 'mysql-cybermouse.alwaysdata.net'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}

# Static files
STATIC_URL = '/static/'
if not DEBUG:
    STATIC_ROOT = BASE_DIR / 'staticfiles'

# Authentication
LOGIN_REDIRECT_URL = '/home/'
LOGIN_URL = '/login/'

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Backend Configuration for Sendmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'  # Assuming sendmail is on localhost
EMAIL_PORT = 25  # Default port for sendmail
EMAIL_USE_TLS = False  # Sendmail usually does not require TLS
DEFAULT_FROM_EMAIL = 'webmaster@localhost'  # Replace with a valid email address
