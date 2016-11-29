"""Test all utils."""

from django.test import TestCase
from django.contrib.sites.models import Site

from geokey.users.tests.model_factories import UserFactory

from geokey_wegovnow.utils import make_email, generate_fake_email


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
