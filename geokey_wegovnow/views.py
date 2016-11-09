"""All views for the WeGovNow extension."""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from requests import get

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from braces.views import LoginRequiredMixin
from allauth.socialaccount import app_settings

from geokey_wegovnow.renderers import RawHTMLRenderer


# ###########################
# ADMIN VIEWS
# ###########################

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


# ###########################
# PUBLIC API
# ###########################

class UWUMNavigationAPIView(APIView):
    """API endpoint for the WeGovNow navigation."""

    renderer_classes = (JSONRenderer, RawHTMLRenderer)
    uwum_settings = app_settings.PROVIDERS.get('uwum', {})

    def get(self, request, format=None):
        """GET method for the view."""
        navigation_url = self.uwum_settings.get('NAVIGATION_URL')
        if not navigation_url:
            return Response(
                {'error': 'URL to UWUM navigation not set'},
                status=status.HTTP_404_NOT_FOUND)

        client_id = None
        if hasattr(request, 'client_id'):
            client_id = request.client_id

        headers = None
        if hasattr(request, 'uwum_access_token'):
            access_token = request.uwum_access_token
            headers = {'Authorization': 'Bearer %s' % access_token}

        response = get(
            '%s?format=%s&client_id=%s' % (
                navigation_url,
                request.accepted_renderer.format,
                client_id),
            headers=headers)

        if response.status_code == 200:
            if request.accepted_renderer.format != 'raw_html':
                response = response.json()
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'UWUM navigation not found'},
                status=status.HTTP_404_NOT_FOUND)
