import os
from pathlib import Path
from decouple import config

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

ROOT_URLCONF = 'mickey.urls'

SECRET_KEY = config('SECRET_KEY', default='fallback_key')

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'saes5.onrender.com']

# --- Static files ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'mousey' / 'static']  # ou BASE_DIR / 'static'
STATIC_ROOT = BASE_DIR / 'staticfiles'

AUTH_USER_MODEL = 'auth.User'

LOGIN_REDIRECT_URL = '/home/'
LOGIN_URL = '/login/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Utilisation de MySQL
        'NAME': 'cybermouse_db',              # Nom de la base de données
        'USER': '384089',                     # Nom d'utilisateur
        'PASSWORD': 'A(h0U1ch0U!',            # Mot de passe
        'HOST': 'mysql-cybermouse.alwaysdata.net',  # Hôte
        'PORT': '3306',                       # Port MySQL
    }
}

# --- Installed apps ---
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
]

# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_otp.middleware.OTPMiddleware',
]

# --- Templates ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# --- Configuration du SMTP ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.alwaysdata.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'cybermouse@alwaysdata.net'  # Nom d'utilisateur SMTP
EMAIL_HOST_PASSWORD = 'A(h0U1ch0U!'             # Mot de passe SMTP
DEFAULT_FROM_EMAIL = 'cybermouse@alwaysdata.net'

# --- Authentication and security ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

X_FRAME_OPTIONS = 'DENY'

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# --- Other settings ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID', default='your_account_sid')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', default='your_auth_token')
TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER', default='+1234567890')