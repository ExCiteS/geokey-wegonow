"""All middleware for the WeGovNow extension."""

from importlib import import_module
from datetime import datetime
from pytz import utc

from django.shortcuts import redirect
from django.http import JsonResponse
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.views import APIView

from allauth.socialaccount.models import SocialToken
from allauth_uwum.views import UWUMAdapter, UWUMView


class WeGovNowMiddleware(object):
    """WeGovNow middleware."""

    def ___get_uwum_view(self, request):
        """Get the UWUM view."""
        view = UWUMView()
        view.request = request
        view.adapter = UWUMAdapter(view.request)
        return view

    def __get_access_token(self, request):
        """Get the access token."""
        try:
            now = datetime.utcnow().replace(tzinfo=utc)
            access_token = SocialToken.objects.filter(
                account__user=request.user,
                account__provider='uwum').latest('id')
            if access_token.expires_at <= now:
                access_token = self.__refresh_access_token(
                    request, access_token)
        except SocialToken.DoesNotExist:
            return None

        return access_token

    def __refresh_access_token(self, request, access_token):
        """Refresh the access token."""
        view = self.___get_uwum_view(request)
        client = view.get_client(view.request, access_token.app)

        token_secret = access_token.token_secret
        refreshed_token = client.refresh_access_token(token_secret)
        refreshed_token = view.adapter.parse_token(refreshed_token)

        access_token.token = refreshed_token.token
        access_token.expires_at = refreshed_token.expires_at
        access_token.save()

        return access_token

    def process_request(self, request):
        """Process the request."""
        request.unauthorized = False

        if hasattr(request, 'user') and not request.user.is_anonymous():
            access_token = self.__get_access_token(request)
            if access_token:
                request.access_token = access_token.token
            else:
                request.unauthorized = True

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Process the response."""
        if request.unauthorized:
            module = import_module(view_func.__module__)
            if issubclass(getattr(module, view_func.__name__), APIView):
                return JsonResponse(
                    {'error': 'Invalid UWUM access token used'},
                    status=status.HTTP_401_UNAUTHORIZED)
            else:
                account_logout_path = reverse('account_logout')
                if request.path != account_logout_path:
                    return redirect(account_logout_path)
