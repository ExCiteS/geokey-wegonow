"""All views for the WeGovNow extension."""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from requests import get

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from braces.views import LoginRequiredMixin
from allauth.socialaccount import app_settings


class UWUMProfileSettingsView(LoginRequiredMixin, TemplateView):
    """API endpoint for the UWUM profile settings (redirection)."""

    template_name = 'base.html'
    uwum_settings = app_settings.PROVIDERS.get('uwum', {})

    def get(self, request):
        """GET method for the view."""
        if hasattr(request, 'member_id'):
            url = '%s/member/show/%s.html' % (
                self.uwum_settings.get('REGULAR_URL', ''),
                request.member_id)
        else:
            url = reverse('account_logout')

        return redirect(url)


class UWUMNavigationAPIView(APIView):
    """API endpoint for the WeGovNow navigation."""

    uwum_settings = app_settings.PROVIDERS.get('uwum', {})

    def get(self, request):
        """GET method for the view."""
        navigation_url = self.uwum_settings.get('NAVIGATION_URL')
        if not navigation_url:
            return Response(
                {'error': 'URL to UWUM navigation not set'},
                status=status.HTTP_404_NOT_FOUND)

        headers = None

        if hasattr(request, 'access_token'):
            headers = {'Authorization': 'Bearer %s' % request.access_token}
        response = get(navigation_url, headers=headers)

        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'UWUM navigation not found'},
                status=status.HTTP_404_NOT_FOUND)
