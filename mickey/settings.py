import os
from pathlib import Path
from decouple import config
# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

ROOT_URLCONF = 'mickey.urls'

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
CSRF_TRUSTED_ORIGINS = [
    'https://saes5.onrender.com',
]

AUTH_USER_MODEL = 'auth.User'

LOGIN_REDIRECT_URL = '/home/'
LOGIN_URL = '/login/'



SECRET_KEY = config('SECRET_KEY', default='fallback_key')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'saes5.onrender.com']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='127.0.0.1'),
        'PORT': config('DB_PORT', default='3306'),
    }
}


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


STATIC_URL = '/static/'

if not DEBUG:
    STATIC_ROOT = BASE_DIR / 'staticfiles'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Assurez-vous que ce répertoire existe et contient vos fichiers HTML.
        'APP_DIRS': True,  # Permet à Django de chercher des templates dans les applications installées.
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

SMTP_CONFIG = {
    # On peut garder des valeurs par défaut pour les éléments non-sensibles
    "SERVER": config('SMTP_SERVER', default="smtp-cybermouse.alwaysdata.net"),
    "PORT": config('SMTP_PORT', default=587, cast=int),

    # Pour les credentials, on ne met PAS de défaut
    "USERNAME": config('SMTP_USERNAME'),
    "PASSWORD": config('SMTP_PASSWORD'),
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = SMTP_CONFIG["SERVER"]
EMAIL_PORT = SMTP_CONFIG["PORT"]
EMAIL_USE_TLS = True
EMAIL_HOST_USER = SMTP_CONFIG["USERNAME"]
EMAIL_HOST_PASSWORD = SMTP_CONFIG["PASSWORD"]

API_CONFIG = {
    "HOST": "O.0.0.0",
    "PORT": 8000,
}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

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