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

MIDDLEWARE_CLASSES += (
    'geokey_wegovnow.middleware.WeGovNowMiddleware',
)

SOCIALACCOUNT_PROVIDERS = {
    'uwum': {
        'NAVIGATION_URL': 'https://wegovnow.liquidfeedback.com/api/1/navigation',
    },
}

TEMPLATES[0]['OPTIONS']['loaders'][:0] = ['geokey_wegovnow.templates.Loader']

STATIC_URL = '/static/'

MEDIA_ROOT = normpath(join(dirname(dirname(abspath(__file__))), 'assets'))
MEDIA_URL = '/assets/'

WSGI_APPLICATION = 'wsgi.application'
