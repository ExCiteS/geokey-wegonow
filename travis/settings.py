"""GeoKey settings."""

from geokey.core.settings.dev import *


DEFAULT_FROM_EMAIL = 'no-reply@travis-ci.org'
ACCOUNT_EMAIL_VERIFICATION = 'optional'

SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxx'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'geokey',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS += (
    'allauth_uwum',
    'geokey_wegovnow',
)

STATIC_URL = '/static/'

MEDIA_ROOT = normpath(join(dirname(dirname(abspath(__file__))), 'assets'))
MEDIA_URL = '/assets/'

WSGI_APPLICATION = 'wsgi.application'
