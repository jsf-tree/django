"""
Django settings for setup project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+71j_ksg*tthain!txl4+li4#e$_-*16to^vjj4wmc(#8j0in0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True # 🌳 Set to False to see 404 debug

ALLOWED_HOSTS = ['*']  # 🌳 changed [] to ['*']


# Application definition

INSTALLED_APPS = [
    'myfirstapp', # 🌳 New app
    'debug_toolbar', # 🌳 Added for debugging
    'polls.apps.PollsConfig', # 🌳 New App - Polls Config File
    'django.contrib.admin', # 🌳 The Admin site
    'django.contrib.auth', # 🌳 An authentication system
    'django.contrib.contenttypes', # 🌳 A framework for content types
    'django.contrib.sessions', # 🌳 Legacy - a session framework
    'django.contrib.messages', # 🌳 A messaging framework
    'django.contrib.staticfiles', # 🌳 A framework for managing static files
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware', # 🌳 Added for debugging
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 🌳 Added for debugging
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

ROOT_URLCONF = 'setup.urls'

# 🌳 Describes how Django will load and render templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True, # 🌳 True = This default setting makes Django to look for templates into each respective app dir called "templates"
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

WSGI_APPLICATION = 'setup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# 🌳 I changed the default sqlite3 DB to PostgreSQL.
DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.postgresql',
        "OPTIONS": {
            "service": "my_service",  # psql --host=localhost --port=5432 --username=django --dbname=db_w_postgis
            "passfile": ".pg_pass",   # must be in format of "hostname:port:database:username:password"
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# 🌳 I set the LANGUAGE_CODE to "de-de" to check the internalization (which abbreviation is "i18n" — funny, i<18 characters>n haha) but then changed it back
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'de-de' 

# 🌳 I set the TIME_ZONE to my time zone
# TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Sao_Paulo' 

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
