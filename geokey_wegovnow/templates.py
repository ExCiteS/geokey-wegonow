"""Additional features for templates."""

from os.path import dirname, join, isfile

from django import VERSION
from django.template.base import Origin
from django.template.loaders.filesystem import Loader as FilesystemLoader


class BaseLoader(FilesystemLoader):
    """Custom base loader for templates."""

    _app_dir = dirname(__file__)

    def _generate_template_source(self, template_name, design):
        """Generate template source."""
        template_source = join(
            self._app_dir,
            'templates',
            design,
            template_name
        )

        if isfile(template_source):
            if VERSION[:2] >= (1, 9):
                template_source = Origin(name=template_source)
            return [template_source]

        return []


class BootstrapLoader(BaseLoader):
    """Custom loader for Material templates."""

    def get_template_sources(self, template_name, template_dirs=None):
        """Override the default GeoKey template with custom Bootstrap UWUM."""
        return self._generate_template_source(template_name, 'bootstrap')


class MaterialLoader(BaseLoader):
    """Custom loader for Material templates."""

    def get_template_sources(self, template_name, template_dirs=None):
        """Override the default GeoKey template with custom Material UWUM."""
        return self._generate_template_source(template_name, 'material')
