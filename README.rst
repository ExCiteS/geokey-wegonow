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
- GeoKey version 1.2 or greater

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

Add the custom WeGovNow middleware for requests and responses:

.. code-block:: python

    MIDDLEWARE_CLASSES += (
        'geokey_wegovnow.middleware.WeGovNowMiddleware',
    )

Extend template loaders with a custom WeGovNow Material:

.. code-block:: python

    TEMPLATES[0]['OPTIONS']['loaders'][:0] = ['geokey_wegovnow.loaders.templates.MaterialLoader']

Or a custom WeGovNow Bootstrap:

.. code-block:: python

    TEMPLATES[0]['OPTIONS']['loaders'][:0] = ['geokey_wegovnow.loaders.templates.BootstrapLoader']

Change UWUM provider settings (change URL accordingly):

.. code-block:: python

    SOCIALACCOUNT_PROVIDERS = {
        'uwum': {
            'CERT': join(dirname(abspath(__file__)), 'uwum.pem'),
            'REGULAR_URL': 'https://wegovnow.liquidfeedback.com',
            'CERT_URL': 'https://wegovnow-cert.liquidfeedback.com',
        },
    }
    SOCIALACCOUNT_PROVIDERS['uwum']['AUTHORIZE_URL'] = '%s/api/1/authorization' % SOCIALACCOUNT_PROVIDERS['uwum']['REGULAR_URL']
    SOCIALACCOUNT_PROVIDERS['uwum']['ACCESS_TOKEN_URL'] = '%s/api/1/token' % SOCIALACCOUNT_PROVIDERS['uwum']['CERT_URL']
    SOCIALACCOUNT_PROVIDERS['uwum']['PROFILE_URL'] = '%s/api/1/info' % SOCIALACCOUNT_PROVIDERS['uwum']['REGULAR_URL']
    SOCIALACCOUNT_PROVIDERS['uwum']['NOTIFY_EMAIL_URL'] = '%s/api/1/notify_email' % SOCIALACCOUNT_PROVIDERS['uwum']['REGULAR_URL']
    SOCIALACCOUNT_PROVIDERS['uwum']['NAVIGATION_URL'] = '%s/api/1/navigation' % SOCIALACCOUNT_PROVIDERS['uwum']['REGULAR_URL']

After all GeoKey migrations are initiated, add the UWUM app (client ID must be the one registered by the UWUM Certificate Authority):

.. code-block:: console

    python manage.py add_uwum_app --id='<client_id>'

Sign up with UWUM account and note your username and email address, then you those details to set yourself as a superuser:

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
