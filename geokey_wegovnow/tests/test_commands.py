"""Test all commands."""

import sys

from StringIO import StringIO

from django.test import TestCase
from django.core import management

from geokey.users.models import User
from geokey.users.tests.model_factories import UserFactory


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
