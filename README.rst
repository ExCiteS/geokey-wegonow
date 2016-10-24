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
- `django-allauth-uwum <https://github.com/ExCiteS/django-allauth-uwum/>`_ 1.0 or greater

Install the extension:

.. code-block:: console

    pip install git+https://github.com/ExCiteS/geokey-wegovnow.git

Add the package to installed apps:

.. code-block:: python

    INSTALLED_APPS += (
        ...
        'geokey_wegovnow',
    )

Add the custom WeGovNow middleware for requests and responses:

.. code-block:: python

    MIDDLEWARE_CLASSES += (
        'geokey_wegovnow.middleware.WeGovNowMiddleware',
    )

Extend template loaders with a custom WeGovNow one:

.. code-block:: python

    TEMPLATES[0]['OPTIONS']['loaders'][:0] = ['geokey_wegovnow.loaders.templates.Loader']

Extend UWUM provider settings, add URL for navigation (change URL accordingly):

.. code-block:: python

    'uwum': {
        ...
        'NAVIGATION_URL': 'https://uwum.wegovnow.eu/api/1/navigation',
    }

You're now ready to go!

Update
------

Update geokey-wegovnow:

.. code-block:: console

    pip install -U git+https://github.com/ExCiteS/geokey-wegovnow.git
