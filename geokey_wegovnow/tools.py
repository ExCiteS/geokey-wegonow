"""All tools for the WeGovNow extension."""

from django.contrib.sites.models import Site
from django.utils.text import slugify

from geokey.users.models import User



def create_random_email(display_name):
    """this method check if the email already exists on the database. If so, 
    it create a new email addres based on retrieve display name
    """

    username = slugify(display_name)
    email = make_emailAddress(
            slugify(username),
            Site.objects.get_current().domain
        )
    
    suffix = 2
    while User.objects.filter(email=email).exists():
        display_name = '%s %s' % (
                slugify(username),
                suffix)
        suffix += 1
        email = make_emailAddress(
            slugify(display_name),
            Site.objects.get_current().domain
        )

    return email

def make_emailAddress(username,domain):
    """This methods creates random email passing email address and domain.
    """

    email =  '{username}@user.{domain}'.format(
        username=username,
        domain=Site.objects.get_current().domain
    )

    return email
