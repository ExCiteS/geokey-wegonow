"""All adapters for the WeGovNow extension."""

from allauth.account.utils import user_username, user_email

from geokey.core.adapters import SocialAccountAdapter
from geokey_wegovnow.utils import generate_display_name, generate_fake_email


class UWUMSocialAccountAdapter(SocialAccountAdapter):
    """UWUM adapter for social accounts."""

    def populate_user(self, request, sociallogin, data):
        """Populate new UWUM user with unique display name and fake email."""
        user = super(UWUMSocialAccountAdapter, self).populate_user(
            request, sociallogin, data)

        username = data.get('username')
        user_username(user, generate_display_name(username))
        user_email(user, generate_fake_email(username))

        return user
