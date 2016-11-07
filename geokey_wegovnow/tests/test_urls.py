"""Test all URLs."""

from django.test import TestCase
from django.core.urlresolvers import reverse, resolve

from geokey_wegovnow import views


class UrlPatternsTests(TestCase):
    """Tests for URL patterns."""

    def test_uwum_profile(self):
        """Test admin page url for UWUM profile settings."""
        view = views.UWUMProfileSettingsView

        reversed_url = reverse('geokey_wegovnow:uwum_profile_settings')
        self.assertEqual(reversed_url, '/admin/profile/settings/')

        resolved_url = resolve('/admin/profile/settings/')
        self.assertEqual(resolved_url.func.func_name, view.__name__)

    def test_api_uwum_navigation(self):
        """Test API url for UWUM navigation."""
        view = views.UWUMNavigationAPIView

        reversed_url = reverse('geokey_wegovnow:api_uwum_navigation')
        self.assertEqual(reversed_url, '/api/wegovnow/navigation/')

        resolved_url = resolve('/api/wegovnow/navigation/')
        self.assertEqual(resolved_url.func.func_name, view.__name__)
