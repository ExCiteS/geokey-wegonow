"""All renderers for the WeGovNow extension."""

from rest_framework.renderers import BaseRenderer


class RawHTMLRenderer(BaseRenderer):
    """Raw HTML renderer."""

    format = 'raw_html'
    media_type = 'text/html'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """Render the response."""
        return data
