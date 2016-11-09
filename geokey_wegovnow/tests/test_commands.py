"""Test all commands."""

import sys

from StringIO import StringIO

from django.conf import settings
from django.test import TestCase
from django.core import management
from django.contrib.sites.shortcuts import get_current_site

from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialApp

from geokey.users.models import User
from geokey.users.tests.model_factories import UserFactory


class AddUWUMAppCommandTest(TestCase):
    """Tests for command `add_uwum_app`."""

    def setUp(self):
        """Set up tests."""
        self.out = StringIO()
        self.err = StringIO()
        sys.stout = self.out
        sys.sterr = self.err

    def test_when_client_id_is_not_provided(self):
        """Test command when client ID is not provided."""
        options = {}
        management.call_command(
            'add_uwum_app',
            stdout=self.out,
            stderr=self.err,
            **options)
        self.assertEquals(self.out.getvalue(), '')
        self.assertTrue('Client ID not provided.' in self.err.getvalue())

    def test_when_social_app_was_not_added_yet(self):
        """Test command when social app was not added yet."""
        options = {'id': 'test-uwum-app'}
        management.call_command(
            'add_uwum_app',
            stdout=self.out,
            stderr=self.err,
            **options)
        self.assertTrue(
            'UWUM app `test-uwum-app` was added.' in self.out.getvalue())
        self.assertTrue(
            'Please configure UWUM in the settings.' in self.out.getvalue())
        self.assertEquals(self.err.getvalue(), '')
        self.assertEquals(SocialApp.objects.count(), 1)
        social_app = SocialApp.objects.latest('pk')
        self.assertEquals(social_app.provider, 'uwum')
        self.assertEquals(social_app.name, 'UWUM')
        self.assertEquals(social_app.client_id, 'test-uwum-app')
        self.assertEquals(social_app.secret, '')
        self.assertEquals(social_app.key, '')

    def test_when_social_app_was_already_added(self):
        """Test command when social app was already added."""
        provider = providers.registry.by_id('uwum')
        social_app = SocialApp.objects.create(
            provider=provider.id,
            name=provider.name,
            client_id='uwum-app-1',
            secret='',
            key='')
        social_app.sites.add(get_current_site(settings.SITE_ID))
        options = {'id': 'uwum-app-2'}
        management.call_command(
            'add_uwum_app',
            stdout=self.out,
            stderr=self.err,
            **options)
        self.assertTrue(
            'UWUM app was updated to `uwum-app-2`.' in self.out.getvalue())
        self.assertEquals(self.err.getvalue(), '')
        self.assertEquals(SocialApp.objects.count(), 1)
        social_app = SocialApp.objects.get(pk=social_app.id)
        self.assertEquals(social_app.provider, 'uwum')
        self.assertEquals(social_app.name, 'UWUM')
        self.assertEquals(social_app.client_id, 'uwum-app-2')
        self.assertEquals(social_app.secret, '')
        self.assertEquals(social_app.key, '')


class SetSuperuserCommandTest(TestCase):
    """Tests for command `set_superuser`."""

    def setUp(self):
        """Set up tests."""
        self.out = StringIO()
        self.err = StringIO()
        sys.stout = self.out
        sys.sterr = self.err

        self.user = UserFactory.create(
            display_name='Test User',
            email='test@email.com',
            is_superuser=False)

    def test_when_username_is_not_provided(self):
        """Test command when username is not provided."""
        options = {'email': self.user.email}
        management.call_command(
            'set_superuser',
            stdout=self.out,
            stderr=self.err,
            **options)
        self.assertEquals(self.out.getvalue(), '')
        self.assertTrue('Username not provided.' in self.err.getvalue())

    def test_when_email_is_not_provided(self):
        """Test command when email is not provided."""
        options = {'username': self.user.display_name}
        management.call_command(
            'set_superuser',
            stdout=self.out,
            stderr=self.err,
            **options)
        self.assertEquals(self.out.getvalue(), '')
        self.assertTrue('Email address not provided.' in self.err.getvalue())

    def test_when_user_is_not_found(self):
        """Test command when user is not found."""
        options = {
            'username': self.user.display_name,
            'email': 'non-existing@email.com'}
        management.call_command(
            'set_superuser',
            stdout=self.out,
            stderr=self.err,
            **options)
        self.assertEquals(self.out.getvalue(), '')
        self.assertTrue('User was not found.' in self.err.getvalue())

        options = {
            'username': 'Non-existing User',
            'email': self.user.email}
        management.call_command(
            'set_superuser',
            stdout=self.out,
            stderr=self.err,
            **options)
        self.assertEquals(self.out.getvalue(), '')
        self.assertTrue('User was not found.' in self.err.getvalue())

    def test_when_user_is_already_superuser(self):
        """Test command when user is already a superuser."""
        self.user.is_superuser = True
        self.user.save()
        options = {
            'username': self.user.display_name,
            'email': self.user.email}
        management.call_command(
            'set_superuser',
            stdout=self.out,
            stderr=self.err,
            **options)
        self.assertEquals(self.out.getvalue(), '')
        self.assertTrue('User is already a superuser.' in self.err.getvalue())

    def test_when_user_is_set_as_the_superuser(self):
        """Test command when user is set as a superuser."""
        options = {
            'username': self.user.display_name,
            'email': self.user.email}
        management.call_command(
            'set_superuser',
            stdout=self.out,
            stderr=self.err,
            **options)
        self.assertTrue('User was set as a superuser.' in self.out.getvalue())
        self.assertEquals(self.err.getvalue(), '')
        user = User.objects.get(pk=self.user.id)
        self.assertEquals(user.is_superuser, True)
