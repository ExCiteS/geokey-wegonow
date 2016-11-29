"""Forms for users."""
from django import forms

from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount import app_settings

from .tools import create_random_email

from geokey.users.models import User

# from geokey.users.models import User


class SignupForm(forms.Form):

    display_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):

        self.sociallogin = kwargs.pop('sociallogin')
        initial = get_adapter().get_signup_form_initial_data(
            self.sociallogin)
        print initial
        if initial['email'] == '':
            username = initial['username']
            email = create_random_email(username)
            initial['email'] = email
        kwargs.update({
            'initial': initial
            })
        super(SignupForm, self).__init__(*args, **kwargs)
