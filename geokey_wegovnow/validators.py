"""All validators for the WeGovNow extension."""

from oauth2_provider.oauth2_validators import OAuth2Validator
from allauth.socialaccount.models import SocialAccount
from allauth_uwum.views import UWUMAdapter, UWUMView


class UWUMOAuth2Validator(OAuth2Validator):
    """UWUM OAuth2 validator."""

    def validate_bearer_token(self, token, scopes, request):
        """Check bearer token provided with the request."""
        if not token:
            return False

        if 'HTTP_UWUM' in request.headers:
            view = UWUMView()
            view.request = request
            view.adapter = UWUMAdapter(view.request)

            response = view.adapter.validate_user(token)
            if response.status_code == 200:
                response = response.json()
                uid = response.get('member', {}).get('id')
                try:
                    account = SocialAccount.objects.select_related('user').get(
                        uid=uid,
                        provider='uwum')
                    request.user = account.user
                    request.scopes = scopes
                    return True
                except SocialAccount.DoesNotExist:
                    pass

            return False

        return super(UWUMOAuth2Validator, self).validate_bearer_token(
            token, scopes, request)
