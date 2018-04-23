#from django.test import TestCase
from unittest import TestCase

from geokey_wegovnow.conversions import make_cm_url


class ExternalUrlsConversionTests(TestCase):

    def test_first_plural_removed(self):
        geokey_url = "https://wegovnow-gk-sandona.geokey.org.uk/api/projects/1/contributions/35"
        expected_cm_url_contains = "/project/"
        expected_cm_url_does_not_contain = "/projects/"
        output = make_cm_url(url=geokey_url)
        self.assertIn(expected_cm_url_contains, output)
        self.assertNotIn(expected_cm_url_does_not_contain, output)

    def test_api_removed(self):
        geokey_url = "https://wegovnow-gk-sandona.geokey.org.uk/api/projects/1/contributions/35"
        expected_cm_url_does_not_contain = "/api/"
        output = make_cm_url(url=geokey_url)
        self.assertNotIn(expected_cm_url_does_not_contain, output)

    def test_protocol_preserved(self):
        geokey_url = "https://wegovnow-gk-sandona.geokey.org.uk/api/projects/1/contributions/35"
        expected_cm_url_starts_with = "https://"
        output = make_cm_url(url=geokey_url)
        self.assertEqual(output[0:8], expected_cm_url_starts_with)

    def test_gk_to_cm(self):
        geokey_url = "https://wegovnow-gk-sandona.geokey.org.uk/api/projects/1/contributions/35"
        expected_cm_url_contains = "wegovnow-cm-sandona"
        output = make_cm_url(url=geokey_url)
        self.assertIn(expected_cm_url_contains, output)


