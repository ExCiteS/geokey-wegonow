"""test for tools.py"""

from django.test import TestCase

from geokey.users.tests.model_factories import UserFactory
from ..tools import create_random_email



class test_create_random_email(TestCase):

    def test_when_display_name_ideal(self):
        display_name = 'user1'

        email = create_random_email(display_name)

        self.assertEqual(email, 'user1@user.example.com')

    def test_when_display_name_has_white_space(self):
        display_name = 'user user'
        email = create_random_email(display_name)

        self.assertEqual(email, 'user-user@user.example.com')

    def test_when_display_name_has_white_space_and_capital_letters(self):

        display_name = 'USer User'
        email = create_random_email(display_name)

        self.assertEqual(email, 'user-user@user.example.com')

    def test_when_display_name_already_exists(self):
        display_name = 'superuser'
        user_new = UserFactory.create(
            display_name=display_name,
            email="superuser@user.example.com")

        email = create_random_email(display_name)

        self.assertNotEqual(email, user_new.email)

    def test_when_display_name_has_special_characters(self):
        display_name = "carabassa!!//**"
        email = create_random_email(display_name)
        self.assertEqual(email, 'carabassa@user.example.com')