"""GeoKey settings."""

from geokey.core.settings.dev import *


DEFAULT_FROM_EMAIL = 'no-reply@travis-ci.org'
ACCOUNT_EMAIL_VERIFICATION = 'optional'

SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxx'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'geokey',
        'USER': 'django',
        'PASSWORD': 'django123',
        'HOST': 'localhost',
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
    'geokey_wegovnow.middleware.UWUMMiddleware',
)

OAUTH2_PROVIDER['OAUTH2_VALIDATOR_CLASS'] = 'geokey_wegovnow.validators.UWUMOAuth2Validator'

SOCIALACCOUNT_ADAPTER = 'geokey_wegovnow.adapters.UWUMSocialAccountAdapter'

SOCIALACCOUNT_PROVIDERS = {
    'uwum': {
        'REGULAR_URL': 'https://wegovnow.liquidfeedback.com',
        'CERT_URL': 'https://wegovnow-cert.liquidfeedback.com',
        'API_VERSION': 1,
    },
}
SOCIALACCOUNT_PROVIDERS['uwum']['NAVIGATION_URL'] = '%s/api/%s/navigation' % (
    SOCIALACCOUNT_PROVIDERS.get('uwum', {}).get('REGULAR_URL').rstrip('/'),
    SOCIALACCOUNT_PROVIDERS.get('uwum', {}).get('API_VERSION'),
)
SOCIALACCOUNT_PROVIDERS['uwum']['SETTINGS_URL'] = '%s/member/settings.html' % (
    SOCIALACCOUNT_PROVIDERS.get('uwum', {}).get('REGULAR_URL').rstrip('/')
)

LOGIN_REDIRECT_URL = SOCIALACCOUNT_PROVIDERS['uwum']['SETTINGS_URL']
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = SOCIALACCOUNT_PROVIDERS['uwum']['SETTINGS_URL']

TEMPLATES[0]['OPTIONS']['loaders'][:0] = ['geokey_wegovnow.templates.BootstrapLoader']

STATIC_URL = '/static/'

MEDIA_ROOT = normpath(join(dirname(dirname(abspath(__file__))), 'assets'))
MEDIA_URL = '/assets/'

WSGI_APPLICATION = 'wsgi.application'
