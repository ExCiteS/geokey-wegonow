"""All middleware for the WeGovNow extension."""

from importlib import import_module
from datetime import datetime
from pytz import utc
from requests import post

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib import messages

from allauth.account.adapter import get_adapter
from allauth.socialaccount import app_settings, providers
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth_uwum.views import UWUMAdapter, UWUMView
from rest_framework import status

from geokey.users.models import User
from geokey.users.views import AccountDisconnect

from .tools import create_random_email



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
        except SocialToken.DoesNotExist:
            return None

        if access_token.expires_at <= datetime.utcnow().replace(tzinfo=utc):
            return self._refresh_uwum_access_token(request, access_token)
        else:
            return self._validate_uwum_access_token(request, access_token)

    def _validate_uwum_access_token(self, request, access_token):
        """Validate the UWUM access token."""
        view = self._get_uwum_view(request)
        headers = view.adapter._make_request_headers(access_token)
        params = {'include_member': True}
        url = app_settings.PROVIDERS.get('uwum', {}).get('VALIDATE_URL', '')

        response = post(url, headers=headers, params=params)
        if response.status_code == 200:
            response = response.json()
            extra_data = access_token.account.extra_data

            current_name = extra_data.get('member', {}).get('name')
            uwum_name = response.get('member', {}).get('name')
            if current_name != uwum_name:
                extra_data['member']['name'] = uwum_name
                access_token.account.extra_data = extra_data
                access_token.account.save()

                display_name = uwum_name
                suffix = 2
                while User.objects.filter(display_name=display_name).exists():
                    display_name = '%s %s' % (uwum_name, suffix)
                    suffix += 1

                request.user.display_name = display_name
                request.user.email = create_random_email(display_name)
                request.user.save()

            self._update_uwum_notify_email(request, access_token)

            return access_token

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

    def _update_uwum_notify_email(self, request, access_token):
        """Update the UWUM notify email."""
        view = self._get_uwum_view(request)
        notify_email = view.adapter.get_notify_email(access_token)

        if notify_email and request.user.email != notify_email:
            request.user.email = notify_email
            request.user.save()

            extra_data = access_token.account.extra_data
            extra_data['member']['email'] = notify_email
            access_token.account.extra_data = extra_data
            access_token.account.save()

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
