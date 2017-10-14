.. image:: https://img.shields.io/travis/ExCiteS/geokey-wegovnow/master.svg
    :alt: Travis CI Build Status
    :target: https://travis-ci.org/ExCiteS/geokey-wegovnow

.. image:: https://img.shields.io/coveralls/ExCiteS/geokey-wegovnow/master.svg
    :alt: Coveralls Test Coverage
    :target: https://coveralls.io/r/ExCiteS/geokey-wegovnow

geokey-wegovnow
================

A custom GeoKey extension for `WeGovNow <http://wegovnow.eu/>`_ functionality.

Install
-------

geokey-wegovnow requires:

- Python version 2.7
- GeoKey version 1.3 or greater

Install django-allauth-uwum:

.. code-block:: console

    pip install git+https://github.com/ExCiteS/django-allauth-uwum.git

Install geokey-wegovnow:

.. code-block:: console

    pip install git+https://github.com/ExCiteS/geokey-wegovnow.git

Add both packages to the installed apps (together with Material Design package):

.. code-block:: python

    INSTALLED_APPS += (
        'material',
        'allauth_uwum',
        'geokey_wegovnow',
    )

Configure django-allauth-uwum using the `official documentation <https://github.com/ExCiteS/django-allauth-uwum>`_.

Add the custom UWUM middleware for requests and responses:

.. code-block:: python

    MIDDLEWARE_CLASSES += (
        'geokey_wegovnow.middleware.UWUMMiddleware',
    )

Extend OAuth2 provider settings by setting a custom UWUM validator class:

.. code-block:: python

    OAUTH2_PROVIDER['OAUTH2_VALIDATOR_CLASS'] = 'geokey_wegovnow.validators.UWUMOAuth2Validator'

Extend template loaders with a custom WeGovNow Material:

.. code-block:: python

    TEMPLATES[0]['OPTIONS']['loaders'][:0] = ['geokey_wegovnow.templates.MaterialLoader']

Or a custom WeGovNow Bootstrap:

.. code-block:: python

    TEMPLATES[0]['OPTIONS']['loaders'][:0] = ['geokey_wegovnow.templates.BootstrapLoader']

Change default social acccount adapter to UWUM:

.. code-block:: python

    SOCIALACCOUNT_ADAPTER = 'geokey_wegovnow.adapters.UWUMSocialAccountAdapter'

Set option that UWUM users would be automatically signed up:

.. code-block:: python

    SOCIALACCOUNT_AUTO_SIGNUP = True

Add UWUM provider settings (change URL accordingly):

.. code-block:: python

    SOCIALACCOUNT_PROVIDERS = {
        'uwum': {
            'CERT': join(dirname(abspath(__file__)), 'uwum.pem'),
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

Change default GeoKey redirects:

.. code-block:: python

    LOGIN_REDIRECT_URL = SOCIALACCOUNT_PROVIDERS['uwum']['SETTINGS_URL']
    ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = SOCIALACCOUNT_PROVIDERS['uwum']['SETTINGS_URL']

After all GeoKey migrations are initiated, add the UWUM app (client ID must be the one registered by the UWUM Certificate Authority):

.. code-block:: console

    python manage.py add_uwum_app --id='<client_id>'

Sign up with UWUM account and note your screen name (not login name!) and email address, then use those details to set yourself as a superuser:

.. code-block:: console

    python manage.py set_superuser --username='<your_username>' --email='<your_email>'

You're now ready to go!

Update
------

Update geokey-wegovnow:

.. code-block:: console

    pip install -U git+https://github.com/ExCiteS/geokey-wegovnow.git

Test
----

Run tests:

.. code-block:: console

    python manage.py test geokey_wegovnow

Check code coverage:

.. code-block:: console

    coverage run --source=geokey_wegovnow manage.py test geokey_wegovnow
    coverage report -m --omit=*/tests/*,*/migrations/*
