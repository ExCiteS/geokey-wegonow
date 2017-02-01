"""Test all utils."""

from django.test import TestCase
from django.http import HttpRequest
from django.contrib.sites.models import Site

from allauth_uwum.views import UWUMAdapter, UWUMView

from geokey.users.tests.model_factories import UserFactory

from geokey_wegovnow.utils import (
    get_uwum_view,
    make_email,
    generate_fake_email,
)


class GetUWUMViewTest(TestCase):
    """Tests for method `get_uwum_view`."""

    def test_method(self):
        """Test method."""
        request = HttpRequest()
        view = get_uwum_view(request)
        self.assertEqual(view.request, request)
        self.assertTrue(isinstance(view, UWUMView))
        self.assertTrue(isinstance(view.adapter, UWUMAdapter))


class MakeEmailTest(TestCase):
    """Tests for method `make_email`."""

    def setUp(self):
        """Set up tests."""
        self.domain = Site.objects.get_current().domain

    def test_method(self):
        """Test method."""
        email = make_email('Tom Black')
        self.assertEqual(email, 'tom-black@user.%s' % self.domain)

        email = make_email('skanhunt_42')
        self.assertEqual(email, 'skanhunt_42@user.%s' % self.domain)

        email = make_email('It\s Me!')
        self.assertEqual(email, 'its-me@user.%s' % self.domain)


class GenerateFakeEmailTest(TestCase):
    """Tests for method `generate_fake_email`."""

    def setUp(self):
        """Set up tests."""
        self.domain = Site.objects.get_current().domain

    def test_when_email_does_not_exist_yet(self):
        """Test method when email is not in use yet."""
        email = generate_fake_email('Tom Black')
        self.assertEqual(email, 'tom-black@user.%s' % self.domain)

    def test_when_email_already_exists(self):
        """Test method when email is already in use."""
        UserFactory.create(
            display_name='Tom Black',
            email='tom-black@user.%s' % self.domain)

        email = generate_fake_email('Tom Black!')
        self.assertEqual(email, 'tom-black-2@user.%s' % self.domain)
