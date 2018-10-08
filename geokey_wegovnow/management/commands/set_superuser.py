"""Command `set_superuser`."""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from optparse import make_option

from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialAccount


class Command(BaseCommand):
    """Set user as a superuser."""

    help = 'Set user as a superuser.'

    def add_arguments(self, parser):

        parser.add_argument(
            '--username',
            action='store',
            dest='username',
            default=None,
            help='Make a user with this username a superuser.'
        )

        parser.add_argument(
            '--email',
            action='store',
            dest='email',
            default=None,
            help='Make a user with this email address a superuser.'
        )

    def handle(self, *args, **options):
        """Handle the command."""
        if not options['username']:
            self.stderr.write('Username not provided.')
        if not options['email']:
            self.stderr.write('Email address not provided.')

        if options['username'] and options['email']:
            user = None
            for account in SocialAccount.objects.all():
                member = account.extra_data.get('member', {})
                if (member.get('name') == options['username'] and
                    member.get('email') == options['email']):
                    user = account.user
                    break

            if user:
                if user.is_superuser:
                    self.stderr.write('User is already a superuser.')
                else:
                    user.is_superuser = True
                    user.save()
                    self.stdout.write('User was set as a superuser.')
            else:
                self.stderr.write('User was not found.')
