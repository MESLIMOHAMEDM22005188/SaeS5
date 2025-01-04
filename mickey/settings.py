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

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'votre_account_sid')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', 'votre_auth_token')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '+33XXXXXXXXX')

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
    "SERVER": "smtp-cybermouse.alwaysdata.net",
    "PORT": 587,
    "USERNAME": os.getenv("SMTP_USERNAME", "cybermouse@alwaysdata.net"),
    "PASSWORD": os.getenv("SMTP_PASSWORD", "A(h0U1ch0U!"),
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

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'votre_account_sid')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', 'votre_auth_token')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '+1 904 637 7917')
# Sécurise les cookies de sessionSESSION_COOKIE_SECURE = True
# Empêche l'accès aux cookies via JavaScript
SESSION_COOKIE_HTTPONLY = True
# Options possibles : 'Lax', 'Strict', 'None'
SESSION_COOKIE_SAMESITE = 'Lax'
# La session expire à la fermeture du navigateur
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# Durée de vie en secondes (ici, 1 heure)
SESSION_COOKIE_AGE = 3600

# Utilise HTTPS pour tous les cookies (les cookies ne seront transmis qu'à travers des connexions sécurisées).
CSRF_COOKIE_SECURE = True

# Empêche JavaScript d'accéder aux cookies CSRF.
CSRF_COOKIE_HTTPONLY = True

# Définir la politique SameSite pour les cookies CSRF.
CSRF_COOKIE_SAMESITE = 'Lax'

# Protège contre le "clickjacking".
X_FRAME_OPTIONS = 'DENY'

# Redirige automatiquement vers HTTPS.
SECURE_SSL_REDIRECT = True  # Redirige automatiquement les requêtes HTTP vers HTTPS

# Active le HSTS (HTTP Strict Transport Security) pour forcer les navigateurs à n'utiliser que HTTPS.
SECURE_HSTS_SECONDS = 31536000  # Durée d'activation (1 an)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Applique le HSTS aux sous-domaines
SECURE_HSTS_PRELOAD = True  # Prépare le site pour le préchargement HSTS

# Utilisation du backend de session par défaut qui stocke les sessions sur le serveur
SESSION_ENGINE = 'django.contrib.sessions.backends.db'