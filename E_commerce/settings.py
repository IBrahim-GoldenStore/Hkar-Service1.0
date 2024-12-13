"""
Django settings for E_commerce project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

from decouple import config



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =  config('secret')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['www.hkarsevice.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'online_store',
    'accounts',
    'anymail'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.middleware.LogoutMiddleware',
]

ROOT_URLCONF = 'E_commerce.urls'

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

WSGI_APPLICATION = 'E_commerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'accounts.backends.Backend_Perso',
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = '/accounts/Connexion/'
# LOGIN_REDIRECT_URL='/online_store/index/'


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

MEDIA_URL = '/media/'  # pour le telechargement des fichiers images et media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if DEBUG  == True:
    EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND= 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST= 'smtp.gmail.com'
    EMAIL_HOST_USER=config('email')
    EMAIL_HOST_PASSWORD=config('motdepasse')
    EMAIL_PORT=587
    EMAIL_USE_TLS= True

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True  # Assure que le cookie CSRF est uniquement envoyé via HTTPS
SESSION_COOKIE_SECURE = True  # Assure que le cookie de session est uniquement envoyé via HTTPS
SESSION_COOKIE_HTTPONLY = True


SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 30*24*60*60
SESSION_SAVE_EVERY_REQUEST = True

X_FRAME_OPTIONS='DENY'
X_CONTENT_TYPE_OPTIONS='nosniff'
SECURE_BROWSER_XSS_FILTER= True
SECURE_HSTS_SECONDS = 31536000  # Durée en secondes (par exemple, 1 an)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Appliquer HSTS à tous les sous-domaines
SECURE_HSTS_PRELOAD = True  # Permettre le préchargement HSTS dans les navigateurs

SECURE_SSL_REDIRECT = True

PASSWORD_RESET_TIMEOUT_DAYS=1