"""Command `set_superuser`."""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from optparse import make_option

from django.core.management.base import BaseCommand

from geokey.users.models import User


class Command(BaseCommand):
    """Set user as the superuser."""

    help = 'Set user as the superuser.'

    option_list = BaseCommand.option_list + (
        make_option(
            '--username',
            action='store',
            dest='username',
            default=None,
            help='Make a user with this username the superuser.'
        ),
        make_option(
            '--email',
            action='store',
            dest='email',
            default=None,
            help='Make a user with this email address the superuser.'
        ),
    )

    def handle(self, *args, **options):
        """Handle the command."""
        if not options['username']:
            self.stderr.write('Username not provided.')
        if not options['email']:
            self.stderr.write('Email address not provided.')

        if options['username'] and options['email']:
            try:
                user = User.objects.get(
                    display_name=options['username'],
                    email=options['email']
                )
            except User.DoesNotExist:
                user = None
                self.stderr.write('User was not found.')

            if user:
                if user.is_superuser:
                    self.stderr.write('User is already the superuser.')
                else:
                    user.is_superuser = True
                    user.save()
                    self.stdout.write('User was set as the superuser.')
