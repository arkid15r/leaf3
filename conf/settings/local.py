from conf.settings.base import *

# https://docs.djangoproject.com/en/stable/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': '',
    }
}

# https://docs.djangoproject.com/en/stable/ref/settings/#debug
DEBUG = True
