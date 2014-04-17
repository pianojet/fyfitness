from base import *  # noqa

DEBUG = True

TEMPLATE_DEBUG = True

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

ROOT_SITE_URL = 'http://fyf.justinerictaylor.com/'
