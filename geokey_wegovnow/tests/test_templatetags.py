"""Test all template tags."""

from django.test import TestCase

from allauth.socialaccount.models import SocialApp, SocialAccount

from geokey.users.tests.model_factories import UserFactory
from geokey.users.templatetags.social import get_social_apps

from geokey_wegovnow.templatetags import wegovnow


class TemplateTagsTest(TestCase):
    """Tests for template tags."""

    def test_exclude_uwum_app(self):
        """Test excluding UWUM app."""
        socialapp_1 = SocialApp.objects.create(
            provider='facebook',
            name='Facebook',
            client_id='xxxxxxxxxxxxxxxxxx',
            secret='xxxxxxxxxxxxxxxxxx',
            key=''
        )
        socialapp_2 = SocialApp.objects.create(
            provider='twitter',
            name='Twitter',
            client_id='xxxxxxxxxxxxxxxxxx',
            secret='xxxxxxxxxxxxxxxxxx',
            key=''
        )
        socialapp_3 = SocialApp.objects.create(
            provider='uwum',
            name='UWUM',
            client_id='xxxxxxxxxxxxxxxxxx',
            secret='',
            key=''
        )

        socialapps = wegovnow.exclude_uwum_app(get_social_apps())

        self.assertTrue(socialapp_1 in socialapps)
        self.assertTrue(socialapp_2 in socialapps)
        self.assertFalse(socialapp_3 in socialapps)

    def test_exclude_uwum_accounts(self):
        """Test excluding UWUM accounts."""
        user = UserFactory.create()
        socialaccount_1 = SocialAccount.objects.create(
            user=user,
            provider='facebook',
            uid='5454'
        )
        socialaccount_2 = SocialAccount.objects.create(
            user=user,
            provider='twitter',
            uid='5478'
        )
        socialaccount_3 = SocialAccount.objects.create(
            user=user,
            provider='uwum',
            uid='1547'
        )
        socialaccount_4 = SocialAccount.objects.create(
            user=user,
            provider='uwum',
            uid='5158'
        )

        socialaccounts = SocialAccount.objects.filter(user=user)
        socialaccounts = wegovnow.exclude_uwum_accounts(socialaccounts)

        self.assertTrue(socialaccount_1 in socialaccounts)
        self.assertTrue(socialaccount_2 in socialaccounts)
        self.assertFalse(socialaccount_3 in socialaccounts)
        self.assertFalse(socialaccount_4 in socialaccounts)
