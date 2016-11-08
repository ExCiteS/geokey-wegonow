"""Test all views."""

import json

from django.test import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage

from rest_framework.test import APIRequestFactory

from geokey.users.tests.model_factories import UserFactory

from geokey_wegovnow import views


class UWUMProfileSettingsViewTest(TestCase):
    """Tests for UWUMProfileSettingsView."""

    url = settings.SOCIALACCOUNT_PROVIDERS['uwum']['REGULAR_URL']

    def setUp(self):
        """Set up tests."""
        self.view = views.UWUMProfileSettingsView.as_view()
        self.request = HttpRequest()
        self.request.method = 'GET'

        setattr(self.request, 'session', 'session')
        messages = FallbackStorage(self.request)
        setattr(self.request, '_messages', messages)

    def test_get_with_anonymous(self):
        """
        Accessing the view with AnonymousUser.

        It should redirect to the login page.
        """
        self.request.user = AnonymousUser()
        response = self.view(self.request)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/account/login/', response['location'])

    def test_get_with_user_when_no_uwum_account(self):
        """
        Accessing the view with normal user, when user has no UWUM account.

        It should log user out.
        """
        user = UserFactory.create()
        self.request.user = user
        response = self.view(self.request)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('account_logout'), response['location'])


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

    def test_get_when_retrieving_uwum_navigation_in_json_format(self):
        """Test GET when retrieving UWUM navigation (JSON)."""
        url = '%s?format=json' % self.url
        request_get = self.factory.get(url)
        response = self.view(request_get).render()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('application/json' in response['Content-Type'])

    def test_get_when_retrieving_uwum_navigation_in_raw_html_format(self):
        """Test GET when retrieving UWUM navigation (Raw HTML)."""
        url = '%s?format=raw_html' % self.url
        request_get = self.factory.get(url)
        response = self.view(request_get).render()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('text/html' in response['Content-Type'])
