#!/usr/bin/env python

"""A custom GeoKey extension for WeGovNow functionality."""

from os.path import join
from setuptools import setup, find_packages


name = 'geokey-wegovnow'
version = __import__(name.replace('-', '_')).__version__
repository = join('https://github.com/ExCiteS', name)

setup(
    name=name,
    version=version,
    description='GeoKey extension for WeGovNow functionality',
    url=repository,
    download_url=join(repository, 'tarball', version),
    author='ExCiteS',
    author_email='excites@ucl.ac.uk',
    license='MIT',
    packages=find_packages(exclude=['*.tests', '*.tests.*', 'tests.*']),
    include_package_data=True,
    install_requires=[
        'django-material==0.10.0',
        'geokey',
    ],
)
