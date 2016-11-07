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
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    'allauth_uwum',
    'geokey_wegovnow',
)

MIDDLEWARE_CLASSES += (
    'geokey_wegovnow.middleware.WeGovNowMiddleware',
)

SOCIALACCOUNT_PROVIDERS = {
    'uwum': {
        'REGULAR_URL': 'https://wegovnow.liquidfeedback.com',
        'CERT_URL': 'https://wegovnow-cert.liquidfeedback.com',
    },
}
SOCIALACCOUNT_PROVIDERS['uwum']['AUTHORIZE_URL'] = '%s/api/1/authorization' % SOCIALACCOUNT_PROVIDERS['uwum']['REGULAR_URL']
SOCIALACCOUNT_PROVIDERS['uwum']['ACCESS_TOKEN_URL'] = '%s/api/1/token' % SOCIALACCOUNT_PROVIDERS['uwum']['CERT_URL']
SOCIALACCOUNT_PROVIDERS['uwum']['PROFILE_URL'] = '%s/api/1/info' % SOCIALACCOUNT_PROVIDERS['uwum']['REGULAR_URL']
SOCIALACCOUNT_PROVIDERS['uwum']['NOTIFY_EMAIL_URL'] = '%s/api/1/notify_email' % SOCIALACCOUNT_PROVIDERS['uwum']['REGULAR_URL']
SOCIALACCOUNT_PROVIDERS['uwum']['NAVIGATION_URL'] = '%s/api/1/navigation' % SOCIALACCOUNT_PROVIDERS['uwum']['REGULAR_URL']

TEMPLATES[0]['OPTIONS']['loaders'][:0] = ['geokey_wegovnow.templates.BootstrapLoader']

STATIC_URL = '/static/'

MEDIA_ROOT = normpath(join(dirname(dirname(abspath(__file__))), 'assets'))
MEDIA_URL = '/assets/'

WSGI_APPLICATION = 'wsgi.application'
