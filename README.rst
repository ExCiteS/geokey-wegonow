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

Add both packages to the installed apps:

.. code-block:: python

    INSTALLED_APPS += (
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

Extend UWUM provider settings, add URL for navigation (change URL accordingly):

.. code-block:: python

    'uwum': {
        ...
        'NAVIGATION_URL': 'https://uwum.wegovnow.eu/api/1/navigation',
    }

After all GeoKey migrations are initiated, add the UWUM app (client ID must be the one registered by the UWUM Certificate Authority):

.. code-block:: console

    python manage.py add_uwum_app --id='<client_id>'

Sign up with UWUM account and note your username and email address, then you those details to set yourself as the superuser:

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
