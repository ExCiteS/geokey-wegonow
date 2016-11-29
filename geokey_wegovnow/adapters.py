"""All adapters for the WeGovNow extension."""

from allauth.account.utils import user_email
from allauth.socialaccount import app_settings

from geokey.core.adapters import SocialAccountAdapter

from geokey_wegovnow.tools import generate_fake_email


class UWUMSocialAccountAdapter(SocialAccountAdapter):
    """UWUM adapter for social accounts."""

    def populate_user(self, request, sociallogin, data):
        """Populate user with fake random email address."""
        user = super(UWUMSocialAccountAdapter, self).populate_user(
            request, sociallogin, data)

        username = getattr(user, app_settings.USER_MODEL_USERNAME_FIELD)
        user_email(user, generate_fake_email(username))

        return user
