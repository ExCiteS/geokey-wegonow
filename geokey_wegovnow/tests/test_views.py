"""Test all views."""

import json

from django.test import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse

from rest_framework.test import APIRequestFactory

from geokey_wegovnow import views


class UWUMNavigationAPIViewTest(TestCase):
    """Tests for UWUMNavigationAPIView."""

    url = settings.SOCIALACCOUNT_PROVIDERS['uwum']['NAVIGATION_URL']

    def setUp(self):
        """Set up tests."""
        settings.SOCIALACCOUNT_PROVIDERS['uwum']['NAVIGATION_URL'] = self.url
        self.factory = APIRequestFactory()
        self.view = views.UWUMNavigationAPIView.as_view()
        self.url = reverse('geokey_wegovnow:api_uwum_navigation')
        self.request_get = self.factory.get(self.url)

    def test_get_when_uwum_navigation_not_set(self):
        """Test GET when UWL to UWUM navigation is not set."""
        settings.SOCIALACCOUNT_PROVIDERS['uwum']['NAVIGATION_URL'] = None
        response = self.view(self.request_get).render()
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            content.get('error'),
            'URL to UWUM navigation not set')

    def test_get_when_uwum_navigation_not_found(self):
        """Test GET when UWUM navigation is not found."""
        settings.SOCIALACCOUNT_PROVIDERS['uwum']['NAVIGATION_URL'] += '/test'
        response = self.view(self.request_get).render()
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            content.get('error'),
            'UWUM navigation not found')

    def test_get_when_retrieving_uwum_navigation(self):
        """Test GET when retrieving UWUM navigation."""
        response = self.view(self.request_get).render()
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('result' in content)
        self.assertTrue(isinstance(content.get('result'), list))
