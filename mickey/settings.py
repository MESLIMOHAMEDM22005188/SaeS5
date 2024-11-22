import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

ROOT_URLCONF = 'mickey.urls'

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATICFILES_DIRS = [Path(BASE_DIR) / "static"]
# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    'https://saes5.onrender.com',
]

# Auth settings
AUTH_USER_MODEL = 'auth.User'

LOGIN_REDIRECT_URL = '/home/'

# Secret Key
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-gb6$j!l#(iokk_x+8yq@mo46%g@dai)s+w&2&f%hyk(vrwjmam')

# Debug settings
DEBUG = True

# Allowed Hosts
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'saes5.onrender.com']

# Installed Applications
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
]

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'votre_account_sid')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', 'votre_auth_token')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '+33XXXXXXXXX')

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

# Password Validation
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


# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
