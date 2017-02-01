"""Test all validators."""

from oauthlib.common import Request

from django.test import TestCase

from geokey_wegovnow import validators


class UWUMOAuth2ValidatorTests(TestCase):
    """Tests for UWUM OAuth2 validator."""

    validator = validators.UWUMOAuth2Validator()

    def setUp(self):
        """Set up tests."""
        self.token = 'f34mfSADsf45sada31mF'
        self.scopes = []
        self.headers = {
            'Authorization': 'Bearer %s' % access_token,
            'UWUM': True,
        }
        self.request = Request(
            'https://geokey.org.uk/api/projects/',
            http_method='GET',
            body=None,
            headers=self.headers)

    def test_validate_bearer_token_when_no_token(self):
        """Test checking bearer token when token is not provided."""
        self.assertFalse(validator.validate_bearer_token(
            None,
            self.scopes,
            self.request))
