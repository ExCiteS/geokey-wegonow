# coding=utf-8
"""Non-Django tests for self-contained conversion methods."""
from unittest import TestCase

from geokey_wegovnow.conversions import make_cm_url, get_link_title


class ExternalUrlsConversionTests(TestCase):

    def test_first_plural_removed(self):
        geokey_url = "https://wegovnow-gk-sandona.geokey.org.uk/api/projects/1/contributions/35"
        expected_cm_url_contains = "/project/"
        expected_cm_url_does_not_contain = "/projects/"
        output = make_cm_url(url=geokey_url)
        self.assertIn(expected_cm_url_contains, output)
        self.assertNotIn(expected_cm_url_does_not_contain, output)

    def test_second_plural_removed(self):
        geokey_url = "https://wegovnow-gk-sandona.geokey.org.uk/api/projects/1/contributions/35"
        expected_cm_url_contains = "/contribution/"
        expected_cm_url_does_not_contain = "/contributions/"
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

    def test_numbers_preserved(self):
        geokey_url = "https://wegovnow-gk-sandona.geokey.org.uk/api/projects/1/contributions/35"
        expected_num_at_pos_2 = "1"
        expected_num_at_pos_4 = "35"
        output_address = make_cm_url(url=geokey_url).split('//')[1]
        self.assertEqual(output_address.split('/')[2], expected_num_at_pos_2)
        self.assertEqual(output_address.split('/')[4], expected_num_at_pos_4)

    def test_gk_to_cm(self):
        geokey_url = "https://wegovnow-gk-sandona.geokey.org.uk/api/projects/1/contributions/35"
        expected_cm_url_contains = "wegovnow-cm-sandona"
        output = make_cm_url(url=geokey_url)
        self.assertIn(expected_cm_url_contains, output)


class GetTitleTests(TestCase):

    def test_blank_dict_unknown(self):
        props = {}
        expected_title = "Unknown title"
        output = get_link_title(properties=props)
        self.assertEquals(output, expected_title)

    def test_find_lc_name_field(self):
        props = {'name': 'It could be sweet'}
        expected_title = "It could be sweet"
        output = get_link_title(properties=props)
        self.assertEquals(output, expected_title)

    def test_find_1cap_name_field(self):
        props = {'Name': 'It could be sweet'}
        expected_title = "It could be sweet"
        output = get_link_title(properties=props)
        self.assertEquals(output, expected_title)

    def test_default_to_first_item(self):
        props = {'Strawberries': 'Wandering'}
        expected_title = "Strawberries Wandering"
        output = get_link_title(properties=props)
        self.assertEquals(output, expected_title)

    def test_numeric_keys(self):
        props = {0: 'Two divided by', 1: 'With each other'}
        expected_title = '0 Two divided by'
        output = get_link_title(properties=props)
        self.assertEqual(output, expected_title)

    def test_numeric_values(self):
        props = {'Two divided by': 0, 'With each other': 1}
        expected_title = 'Two divided by 0'
        output = get_link_title(properties=props)
        self.assertEqual(output, expected_title)


class GetLinkTitleNonAsciiCharsTest(TestCase):

    def test_ascii_chars(self):
        props = {'Some normal chars': 'THIS-THING'}
        expected_title = 'Some normal chars THIS-THING'
        output = get_link_title(properties=props)
        self.assertEqual(output, expected_title)

    def test_non_ascii_charts(self):
        props = {'Title': 'Ç-THàNG¡'}
        expected_title = u'Ç-THàNG¡'
        output = get_link_title(properties=props)
        self.assertEqual(expected_title, output)

