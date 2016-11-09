"""Command `add_uwum_app`."""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.sites.shortcuts import get_current_site

from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    """Add UWUM app."""

    help = 'Add UWUM app.'

    option_list = BaseCommand.option_list + (
        make_option(
            '--id',
            action='store',
            dest='id',
            default=None,
            help='Add UWUM app with this ID.'
        ),
    )

    def handle(self, *args, **options):
        """Handle the command."""
        provider = None

        if not options['id']:
            self.stderr.write('Client ID not provided.')
        else:
            try:
                provider = providers.registry.by_id('uwum')
            except KeyError:
                self.stderr.write('django-allauth-uwum is not installed.')

        if provider:
            try:
                social_app = SocialApp.objects.get_current(provider.id)
            except SocialApp.DoesNotExist:
                social_app = None

            if social_app:
                social_app.client_id = options['id']
                social_app.save()
                self.stdout.write(
                    'UWUM app was updated to `%s`.' % options['id'])
            else:
                social_app = SocialApp.objects.create(
                    provider=provider.id,
                    name=provider.name,
                    client_id=options['id'],
                    secret='',
                    key='')
                social_app.sites.add(get_current_site(settings.SITE_ID))
                self.stdout.write('UWUM app `%s` was added.' % options['id'])
                self.stdout.write('Please configure UWUM in the settings.')
