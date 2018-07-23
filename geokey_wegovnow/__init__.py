"""Main initialization for the WeGovNow extension."""

VERSION = (3, 1, 1)
__version__ = '.'.join(map(str, VERSION))


try:
    from geokey.extensions.base import register

    register(
        'geokey_wegovnow',
        'WeGovNow',
        display_admin=False,
        superuser=False,
        version=__version__
    )
except BaseException:
    print 'Please install GeoKey first'
