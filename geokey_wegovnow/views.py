"""All views for the WeGovNow extension."""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from requests import get

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from allauth.socialaccount import app_settings


class NavigationAPIView(APIView):
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
