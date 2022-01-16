"""WSGI (https://wsgi.readthedocs.io/en/latest/) module for the project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings.local')

# https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/#the-application-object
application = get_wsgi_application()
