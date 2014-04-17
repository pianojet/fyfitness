from base import *  # noqa

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