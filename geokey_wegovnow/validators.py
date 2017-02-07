"""All validators for the WeGovNow extension."""

from oauth2_provider.oauth2_validators import OAuth2Validator
from allauth.socialaccount.models import SocialAccount

from geokey_wegovnow.utils import get_uwum_view, sign_up_uwum_user


class UWUMOAuth2Validator(OAuth2Validator):
    """UWUM OAuth2 validator."""

    def validate_bearer_token(self, token, scopes, request):
        """
        Check bearer token provided with the request.

        First, check if token is an UWUM access token. If it is, get the GeoKey
        user associated with the UWUM account. If account does not exist yeat,
        create one automatically. But if token is not validated by UWUM, try
        and validate it with personal GeoKey OAuth2.
        """
        if not token:
            return False

        # Valid UWUM token?
        view = get_uwum_view(request)
        response = view.adapter.validate_user(token)
        if response.status_code == 200:
            response = response.json()
            uid = response.get('member', {}).get('id')

            try:
                # Is related user already created on GeoKey?
                account = SocialAccount.objects.select_related('user').get(
                    uid=uid, provider=view.adapter.get_provider().id)
                user = account.user
            except SocialAccount.DoesNotExist:
                # If no - create one!
                user = sign_up_uwum_user(request, response)

            request.user = user
            request.user.uwum = True
            request.scopes = scopes
            # That's it, we have the user! It's safe to terminate here.
            return True

        # If token is not validated by UWUM, maybe it's GeoKey token?
        return super(UWUMOAuth2Validator, self).validate_bearer_token(
            token, scopes, request)
