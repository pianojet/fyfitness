# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(__file__)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v8fu^_h^kr0#2n#klwgi0=($qu3$(e-9rdv490b*s9igl$q!+!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

LOGIN_EXEMPT_URLS = (
    '/robots.txt$',  # Only applicable to development (DEBUG)
)

# Application definition
PROJECT_APPS = (
    'membership',
    'public_site',
    'registration',
    'blog',
    'message',
    'calendar',
    'autocomplete',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'south',  # Database migration package # http://south.aeracode.org/
) + PROJECT_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),
)

# Most notably il8n and media not included from the defaults.
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.static',
    'django.core.context_processors.csrf',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fyfitness',
        'USER': 'fyfitness',
        'PASSWORD': 'pass123',
        'HOST': '',
        'PORT': '',
        'STORAGE_ENGINE': 'InnoDB',
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

SHELL_PLUS = "ipython"

STATIC_ROOT = os.path.join(PROJECT_PATH, 'media', 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'static'),
)
# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

ACCOUNT_ACTIVATION_DAYS = 7

#ROOT_SITE_URL = 'http://fyfitness.com/'
ROOT_SITE_URL = 'http://fyf.justinerictaylor.com/'

LOGIN_REDIRECT_URL = '/membership/home/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'