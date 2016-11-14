"""All middleware for the WeGovNow extension."""

from importlib import import_module

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib import messages

from allauth.account.adapter import get_adapter
from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth_uwum.views import UWUMAdapter, UWUMView
from rest_framework import status

from geokey.users.views import AccountDisconnect


class WeGovNowMiddleware(object):
    """WeGovNow middleware."""

    def _get_uwum_view(self, request):
        """Get the UWUM view."""
        view = UWUMView()
        view.request = request
        view.adapter = UWUMAdapter(view.request)
        return view

    def _get_uwum_access_token(self, request):
        """Get the UWUM access token."""
        try:
            access_token = SocialToken.objects.filter(
                account__user=request.user,
                account__provider='uwum'
            ).latest('id')
            request.member_id = access_token.account.uid
        except SocialToken.DoesNotExist:
            return None

        return self._refresh_uwum_access_token(request, access_token)

    def _refresh_uwum_access_token(self, request, access_token):
        """Refresh the access token."""
        view = self._get_uwum_view(request)
        client = view.get_client(view.request, access_token.app)

        try:
            refreshed_token = client.refresh_access_token(
                access_token.token_secret)
        except OAuth2Error:
            return None

        refreshed_token = view.adapter.parse_token(refreshed_token)
        access_token.token = refreshed_token.token
        if refreshed_token.token_secret:
            access_token.token_secret = refreshed_token.token_secret
        access_token.expires_at = refreshed_token.expires_at
        access_token.save()

        return access_token

    def _validate_uwum_user(self, request):
        """Validate the UWUM user."""
        if hasattr(request, 'user') and not request.user.is_anonymous():
            if not hasattr(request, 'uwum_access_token'):
                request.uwum_access_token = self._get_uwum_access_token(
                    request)

    def process_request(self, request):
        """Process the request."""
        self._validate_uwum_user(request)

        provider = providers.registry.by_id('uwum')

        try:
            app = SocialApp.objects.get_current(provider.id, request)
            client_id = app.client_id
        except SocialApp.DoesNotExist:
            client_id = None

        request.client_id = client_id

    def process_response(self, request, response):
        """Process the response."""
        self._validate_uwum_user(request)

        if hasattr(request, 'uwum_access_token'):
            if not request.uwum_access_token:
                if request.META['PATH_INFO'].startswith('/api/'):
                    return JsonResponse(
                        {'error': 'Invalid UWUM access token used'},
                        status=status.HTTP_401_UNAUTHORIZED)
                else:
                    messages.error(request, 'You have been signed out.')
                    auth_logout(request)
                    adapter = get_adapter(request)
                    return redirect(adapter.get_logout_redirect_url(request))

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Process the view."""
        try:
            module = import_module(view_func.__module__)
            class_name = getattr(module, view_func.__name__)

            if issubclass(class_name, AccountDisconnect):
                try:
                    account = SocialAccount.objects.get(
                        pk=view_kwargs.get('account_id'),
                        user=request.user)
                    if account.provider == 'uwum':
                        messages.error(
                            request,
                            'The UWUM account cannot be disconnected.')
                        return HttpResponseRedirect(
                            reverse('admin:userprofile'))
                except:
                    pass
        except:
            pass
