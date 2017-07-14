"""All views for the WeGovNow extension."""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from requests import get

from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from braces.views import LoginRequiredMixin
from allauth.socialaccount import app_settings

from geokey_wegovnow.middleware import UWUMMiddleware
from geokey_wegovnow.renderers import RawHTMLRenderer
from geokey.core.models import LoggerHistory

from .logger import create_event, send_events
from .base import ONTOMAP_MODELS

import json
import ast



# ###########################
# ADMIN VIEWS
# ###########################


class UWUMProfileSettingsView(LoginRequiredMixin, TemplateView):
    """API endpoint for the UWUM profile settings (redirection)."""

    template_name = 'base.html'
    uwum_settings = app_settings.PROVIDERS.get('uwum', {})

    def get(self, request):
        """GET method for the view."""
        url = '%s/member/settings.html' % (
            self.uwum_settings.get('REGULAR_URL', ''))
        return redirect(url)


# ###########################
# PUBLIC API
# ###########################

class UWUMNavigationAPIView(APIView):
    """API endpoint for the UWUM navigation."""

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

        if (not hasattr(request, 'uwum_access_token') and
                not request.user.is_anonymous()):
            middleware = UWUMMiddleware()
            middleware._validate_uwum_user(request)

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


@receiver(post_save, sender=LoggerHistory)
def post_historical_logger(sender, instance, created, **kwargs):
    """Check when a new logger is created for the ONTOMAP_MODELS."""
    print ("*************************************** post historical logger ", instance.action['id'])
    print ("*************************************** post historical logger ", instance.action['class'])
    if instance.action['class'] in ONTOMAP_MODELS:
        print ("*************************************** before send event ")
        event = create_event(
            instance,
            instance.action['class'],
            instance.action['id'])

        print(":::::::::::::::::::: event is ", event)
        # at this point, the event is still a string with single quotes, based on the text in base.py
        # so now need to convert the string to json by replacing the single quotes with double quotes

        print("zzzzzzzzzzzzzzzzzzzzzzz33", event.replace("'","\""))
        event = event.replace("'","\"")
        # the JSON doesn't need encoding - it should be sent as a string as part of the POST statement
        #send_events(json.loads(event))
        send_events(event)
        print ("*************************************** after send event ");

