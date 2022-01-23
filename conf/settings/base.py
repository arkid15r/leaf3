"""Project settings base."""

import os
from pathlib import Path

import environ

ugettext = lambda s: s

# Paths.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR / 'apps'

# https://django-environ.readthedocs.io/en/latest/tips.html
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, 'conf/.env'))

# Installed applications.
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
]

EXTERNAL_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'bootstrap_datepicker_plus',
    'compressor',
    'crispy_forms',
    'django_neomodel',
]

PROJECT_APPS = [
    'apps.core',
    'apps.schema',
    'apps.tree',
    'apps.user',
]

# https://docs.djangoproject.com/en/stable/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + PROJECT_APPS

# Authentication.
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'user.User'

# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# https://docs.djangoproject.com/en/stable/ref/settings/#login-url
LOGIN_URL = 'account_login'

# Databases.
# https://docs.djangoproject.com/en/stable/ref/databases/
DATABASES = {
    'default': env.db(),
}

# https://docs.djangoproject.com/en/stable/ref/settings/#atomic-requests
DATABASES['default']['ATOMIC_REQUESTS'] = True

# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# https://docs.djangoproject.com/en/stable/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)

# Middleware.
# https://docs.djangoproject.com/en/stable/ref/settings/#middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Templates.
# https://docs.djangoproject.com/en/stable/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(APPS_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# https://docs.djangoproject.com/en/stable/ref/settings/#secret-key
SECRET_KEY = env.str('SECRET_KEY')

# Language, i18, l10n, timezones.
# https://docs.djangoproject.com/en/stable/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

LANGUAGES = (('en', ugettext('English')),)

# https://docs.djangoproject.com/en/stable/ref/settings/#locale-paths
LOCALE_PATHS = [os.path.join(APPS_DIR, 'locale')]

# https://docs.djangoproject.com/en/stable/ref/settings/#time-zone
TIME_ZONE = 'UTC'

# https://docs.djangoproject.com/en/stable/ref/settings/#use-i18n
USE_I18N = True

# https://docs.djangoproject.com/en/stable/ref/settings/#use-l10n
USE_TZ = True

# Media files.
# https://docs.djangoproject.com/en/stable/ref/settings/#media-root
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# https://docs.djangoproject.com/en/stable/ref/settings/#media-url
MEDIA_URL = 'media/'

# Static files.
# https://docs.djangoproject.com/en/stable/ref/settings/#static-root
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# https://docs.djangoproject.com/en/stable/ref/settings/#static-url
STATIC_URL = '/static/'

# https://docs.djangoproject.com/en/stable/ref/settings/#staticfiles-dirs
STATICFILES_DIRS = [os.path.join(APPS_DIR, 'static')]

# https://docs.djangoproject.com/en/dev/ref/settings/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

# Site settings.
# https://docs.djangoproject.com/en/stable/ref/settings/#site-id
SITE_ID = 1

# https://docs.djangoproject.com/en/stable/ref/settings/#wsgi-application
WSGI_APPLICATION = 'conf.wsgi.application'

# URLs.
# https://docs.djangoproject.com/en/stable/ref/settings/#root-urlconf
ROOT_URLCONF = 'conf.urls'

# Admin control panel URL.
ADMIN_URL = 'admin/'

# django-allauth
ALL_AUTH_URL = 'auth/'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_FORMS = {
    'login': 'apps.core.forms.LoginForm',
    'signup': 'apps.core.forms.SignupForm',
}
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 3
# TODO(ark): go back to the default POST approach after fixing the page layout.
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'

#django-compressor
# https://django-compressor.readthedocs.io/en/stable/settings.html#django.conf.settings.COMPRESS_ENABLED
COMPRESS_ENABLED = env.bool('COMPRESS_ENABLED', default=False)

# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_OFFLINE = False

# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_FILTERS
COMPRESS_FILTERS = {
    'css': [
        'compressor.filters.css_default.CssAbsoluteFilter',
        'compressor.filters.cssmin.rCSSMinFilter',
    ],
    'js': ['compressor.filters.jsmin.JSMinFilter'],
}

# https://django-compressor.readthedocs.io/en/stable/settings.html?#django.conf.settings.COMPRESS_OUTPUT_DIR
COMPRESS_OUTPUT_DIR = 'compress'

# https://django-compressor.readthedocs.io/en/stable/settings.html?highlight=scss#django.conf.settings.COMPRESS_PRECOMPILERS
COMPRESS_PRECOMPILERS = (('text/scss', 'sass {infile} {outfile}'),)

# https://django-compressor.readthedocs.io/en/stable/settings.html#django.conf.settings.COMPRESS_STORAGE
COMPRESS_STORAGE = 'compressor.storage.GzipCompressorFileStorage'

# https://django-compressor.readthedocs.io/en/stable/settings.html?#django.conf.settings.COMPRESS_URL
COMPRESS_URL = STATIC_URL

# django-crispy-forms
# https://django-crispy-forms.readthedocs.io/en/stable/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap4'

NEOMODEL_NEO4J_BOLT_URL = env.str('NEO4J_DATABASE_URL')

# shortuuid
# https://github.com/skorokithakis/shortuuid
SHORT_UUID_ALPHABET = '23456789abcdefghijkmnopqrstuvwxyz'
SHORT_UUID_LENGTH = 10
