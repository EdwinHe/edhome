"""
Django settings for edhome project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!0mo@7ch)2%91^e3=x+&8son839z@ng*60a!zu*1)tzsg#v8m!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ozio',
    'rest_framework',  # REST Framework
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'edhome.urls'

WSGI_APPLICATION = 'edhome.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        ## SQLite3
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

        ## MySQL
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'edhome',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '',    
        
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Australia/ACT'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# Setup below two allows main templates and static to be included.
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'edhome/templates')]
STATICFILES_DIRS  = (os.path.join(BASE_DIR, 'edhome/static'),)


# Logging setup
from datetime import datetime
log_file_name = os.path.join(BASE_DIR, 'logs', 'EdCo.' + datetime.now().strftime('%Y%m%d_%H') + '.log')
db_log_file_name = os.path.join(BASE_DIR, 'logs', 'EdCo.db.' + datetime.now().strftime('%Y%m%d_%H') + '.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': log_file_name,
            'formatter': 'verbose'
        },
        'db_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': db_log_file_name,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file_log'],
            'propagate' : False,
            'level':'DEBUG',
        },
        'django.db': {
            'handlers':['db_log'],
            'propagate' : False,
            'level':'DEBUG',
        },
        'edhome': {
            'handlers': ['file_log'],
            'propagate' : False,
            'level': 'DEBUG',
        },
        'ozio': {
            'handlers': ['file_log'],
            'level': 'DEBUG',
        },
    }
}

