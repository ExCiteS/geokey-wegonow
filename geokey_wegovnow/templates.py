"""Additional features for templates."""

from os.path import dirname, join, isfile

from django import VERSION
from django.template.base import Origin
from django.template.loaders.filesystem import Loader as FilesystemLoader


class Loader(FilesystemLoader):
    """Custom loader for templates."""

    def get_template_sources(self, template_name, template_dirs=None):
        """Override the default GeoKey template with a custom WeGovNow one."""
        app_dir = dirname(__file__)
        template_source = join(app_dir, 'templates', template_name)

        if isfile(template_source):
            if VERSION[:2] >= (1, 9):
                template_source = Origin(name=template_source)
            return [template_source]

        return []
