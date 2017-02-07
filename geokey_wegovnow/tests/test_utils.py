"""Test all utils."""

from importlib import import_module

from django.test import TestCase
from django.conf import settings
from django.http import HttpRequest
from django.contrib.sites.models import Site

from allauth.socialaccount.models import SocialAccount
from allauth_uwum.views import UWUMAdapter, UWUMView

from geokey.users.models import User
from geokey.users.tests.model_factories import UserFactory
from geokey_wegovnow.utils import (
    get_uwum_view,
    sign_up_uwum_user,
    make_email_address,
    generate_display_name,
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


class SignUpUWUMUserTest(TestCase):
    """Tests for method `sign_up_uwum_user`."""

    def test_method(self):
        """Test method."""
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)

        response = {
            'member': {
                'id': '129',
                'name': 'New User'
            }
        }
        user = sign_up_uwum_user(request, response)
        socialaccount = SocialAccount.objects.latest('pk')
        self.assertEqual(socialaccount.provider, 'uwum')
        self.assertEqual(socialaccount.uid, '129')
        self.assertTrue(isinstance(socialaccount.user, User))
        self.assertEqual(socialaccount.user.display_name, 'New User')
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.display_name, 'New User')

        response = {
            'member': {
                'id': '130',
                'name': 'New User'  # Just in case UWUM gives same member name
            }
        }
        user = sign_up_uwum_user(request, response)
        socialaccount = SocialAccount.objects.latest('pk')
        self.assertEqual(socialaccount.provider, 'uwum')
        self.assertEqual(socialaccount.uid, '130')
        self.assertTrue(isinstance(socialaccount.user, User))
        self.assertEqual(socialaccount.user.display_name, 'New User 2')
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.display_name, 'New User 2')


class MakeEmailAddressTest(TestCase):
    """Tests for method `make_email_address`."""

    def setUp(self):
        """Set up tests."""
        self.domain = Site.objects.get_current().domain

    def test_method(self):
        """Test method."""
        email = make_email_address('Tom Black')
        self.assertEqual(email, 'tom-black@user.%s' % self.domain)

        email = make_email_address('skanhunt_42')
        self.assertEqual(email, 'skanhunt_42@user.%s' % self.domain)

        email = make_email_address('It\s Me!')
        self.assertEqual(email, 'its-me@user.%s' % self.domain)


class GenerateDisplayNameTest(TestCase):
    """Tests for method `generate_display_name`."""

    def setUp(self):
        """Set up tests."""
        self.domain = Site.objects.get_current().domain

    def test_when_display_name_does_not_exist_yet(self):
        """Test method when display name is not in use yet."""
        display_name = generate_display_name('Tom Black')
        self.assertEqual(display_name, 'Tom Black')

    def test_when_display_name_already_exists(self):
        """Test method when display name is already in use."""
        UserFactory.create(
            display_name='Tom Black',
            email='tom-black@user.%s' % self.domain)

        display_name = generate_display_name('Tom Black')
        self.assertEqual(display_name, 'Tom Black 2')


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
