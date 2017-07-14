"""All utils for the WeGovNow extension."""

from django.utils.text import slugify
from django.contrib.sites.models import Site

from allauth.socialaccount.adapter import get_adapter
from allauth_uwum.views import UWUMAdapter, UWUMView

from geokey.users.models import User


def get_uwum_view(request):
    """Get the UWUM view (with adapter) passing the request."""
    view = UWUMView()
    view.request = request
    view.adapter = UWUMAdapter(view.request)
    return view


def sign_up_uwum_user(request, response):
    """Sign up the UWUM user automatically on GeoKey."""
    view = get_uwum_view(request)
    provider = view.adapter.get_provider()
    sociallogin = provider.sociallogin_from_response(request, response)
    return get_adapter(request).save_user(request, sociallogin, form=None)


def make_email_address(username):
    """Make email address using the current domain."""
    return '{username}@user.{domain}'.format(
        username=slugify(username),
        domain=Site.objects.get_current().domain)


def generate_display_name(username):
    """Generate display name for the UWUM user."""
    display_name = username
    suffix = 2
    while User.objects.filter(display_name=display_name).exists():
        display_name = '%s %s' % (username, suffix)
        suffix += 1
    return display_name


def generate_fake_email(username):
    """Generate fake email for the UWUM user."""
    email = make_email_address(username)
    suffix = 2
    while User.objects.filter(email=email).exists():
        email = make_email_address('%s %s' % (username, suffix))
        suffix += 1
    return email
