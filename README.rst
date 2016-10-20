geokey-wegovnow
================

A custom GeoKey extension for `WeGovNow <http://wegovnow.eu/>`_ functionality.

Install
-------

geokey-wegovnow requires:

- Python version 2.7
- GeoKey version 1.2 or greater

Install the extension:

.. code-block:: console

    pip install git+https://github.com/ExCiteS/geokey-wegovnow.git

Add the package to installed apps:

.. code-block:: python

    INSTALLED_APPS += (
        ...
        'geokey_wegovnow',
    )

Extend template loaders with a custom WeGovNow one:

.. code-block:: python

    TEMPLATES[0]['OPTIONS']['loaders'][:0] = ['geokey_wegovnow.loaders.templates.Loader']

You're now ready to go!

Update
------

Update geokey-wegovnow:

.. code-block:: console

    pip install -U git+https://github.com/ExCiteS/geokey-wegovnow.git
