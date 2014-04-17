from base import *  # noqa

DEBUG = True

TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fyfitnessdev',
        'USER': 'fyfitnessdev',
        'PASSWORD': 'pass123',
        'HOST': '',
        'PORT': '',
        'STORAGE_ENGINE': 'InnoDB',
    },
}

ROOT_SITE_URL = 'http://dev.justinerictaylor.com/'

# debug toolbar
INSTALLED_APPS += (
    'debug_toolbar',
    )

INTERNAL_IPS=(
            '127.0.0.1',
            '74.128.247.31',
            )

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        }

TEST_RUNNER_VERBOSE = True
DEBUG_TOOLBAR_PATCH_SETTINGS = False