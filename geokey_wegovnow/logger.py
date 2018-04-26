"""WeGovNow extension OnToMap logger."""

import json
import time

from os import path
from ast import literal_eval
from requests import request

from django.conf import settings
from django.contrib.sites.models import Site

from allauth.socialaccount.models import SocialAccount
from allauth_uwum.provider import UWUMProvider

from geokey.core.signals import get_request
from geokey_wegovnow.base import MAPPINGS


# Default headers for OnToMap
from geokey_wegovnow.conversions import make_cm_url

headers = {'content-type': 'application/json;charset=utf-8'}


def get_cert():
    """Get the UWUM certificate."""
    cert = UWUMProvider.settings.get('CERT')

    if not path.exists(cert):
        raise IOError('UWUM certificate not found')

    return cert


def check_mappings():
    """Get OnToMap mappings."""
    mappings = get_mappings()

    # Send mappings if it does not exist or does not match local mappings
    if (mappings.status_code != 200 or
            literal_eval(mappings.content).get('mappings') != MAPPINGS):
        send_mappings()


def get_mappings():
    """Get OnToMap mappings."""
    cert = get_cert()
    url = settings.ONTOMAP_URLS['MAPPINGS_URL']

    response = request(
        'GET',
        url=url,
        cert=cert)

    return response


def send_mappings():
    """Send OnToMap mappings."""
    cert = get_cert()
    url = settings.ONTOMAP_URLS['MAPPINGS_URL']

    data = {
        'mappings': MAPPINGS
    }

    response = request(
        'POST',
        headers=headers,
        url=url,
        cert=cert,
        data=json.dumps(data))

    return response


def get_events():
    """Get OnToMap events."""
    cert = get_cert()
    url = settings.ONTOMAP_URLS['EVENTS_URL']

    response = request(
        'GET',
        headers=headers,
        url=url,
        cert=cert)

    return response


def make_event(class_name, instance, action):
    """Make OnToMap event."""
    domain = Site.objects.get_current().domain
    uwum_account = SocialAccount.objects.get(
        provider='uwum',
        user=get_request().user)

    activity_objects = []
    visibility_details = []
    details = {}

    # ###########################
    # ADDITIONS FOR PROJECT
    # ###########################

    if class_name == 'Project':
        external_url = '%s/api/projects/%s/' % (
            domain, instance.id)

        if action == 'deleted' or instance.isprivate:
            hidden = True
        else:
            hidden = instance.status == 'active'

        activity_objects.append({
            'type': 'Feature',
            'geometry': None,
            'properties': {
                'hasType': 'Project',
                'name': instance.name,
                'external_url': make_cm_url(external_url),
                'additionalProperties': {
                    'description': instance.description
                }
            }
        })

        visibility_details.append({
            'external_url': make_cm_url(external_url),
            'hidden': hidden
        })

        details['project_id'] = instance.id

    # ###########################
    # ADDITIONS FOR CATEGORY
    # ###########################

    if class_name == 'Category':
        external_url = '%s/api/projects/%s/categories/%s/' % (
            domain, instance.project.id, instance.id)
        hidden = True if action == 'deleted' else instance.status == 'active'

        activity_objects.append({
            'type': 'Feature',
            'geometry': None,
            'properties': {
                'hasType': 'Category',
                'name': instance.name,
                'external_url': make_cm_url(external_url),
                'additionalProperties': {
                    'description': instance.description
                }
            }
        })

        visibility_details.append({
            'external_url': make_cm_url(external_url),
            'hidden': hidden
        })

        details['project_id'] = instance.project.id
        details['category_id'] = instance.id

    # ###########################
    # ADDITIONS FOR CONTRIBUTION
    # ###########################

    if class_name == 'Observation':
        external_url = '%s/api/projects/%s/contributions/%s/' % (
            domain, instance.project.id, instance.id)
        hidden = True if action == 'deleted' else instance.status == 'active'

        geometry = literal_eval(instance.location.geometry.geojson)
        properties = literal_eval(json.dumps(instance.properties))

        activity_objects.append({
            'type': 'Feature',
            'geometry': geometry,
            'properties': {
                'hasType': 'Contribution',
                'name': 'test_name',
                'external_url': make_cm_url(external_url),
                'additionalProperties': properties
            }
        })

        visibility_details.append({
            'external_url': make_cm_url(external_url),
            'hidden': hidden
        })

        details['project_id'] = instance.project.id
        details['category_id'] = instance.category.id

    # ###########################
    # ADDITIONS FOR COMMENT
    # ###########################

    if class_name == 'Comment':
        contribution = instance.commentto
        parent_comment = instance.respondsto or None

        external_url = '%s/api/projects/%s/contributions/%s/comments' % (
            domain, contribution.project.id, contribution.id)
        hidden = True if action == 'deleted' else instance.status == 'active'

        activity_objects.append({
            'type': 'Feature',
            'geometry': None,
            'properties': {
                'hasType': 'Comment',
                'external_url': make_cm_url(external_url),
                'additionalProperties': {
                    'text': instance.text,
                    'responds_to': (
                        None if not parent_comment else parent_comment.id
                    )
                }
            }
        })

        visibility_details.append({
            'external_url': make_cm_url(external_url),
            'hidden': hidden
        })

        details['project_id'] = contribution.project.id
        details['category_id'] = contribution.category.id
        details['contribution_id'] = contribution.id

    # ###########################
    # ADDITIONS FOR MEDIA FILE
    # ###########################

    if class_name == 'MediaFile':
        contribution = instance.contribution

        external_url = '%s/api/projects/%s/contributions/%s/media/%s' % (
            domain, contribution.project.id, contribution.id, instance.id)
        hidden = True if action == 'deleted' else instance.status == 'active'

        if hasattr(instance, 'audio'):
            url = domain + instance.audio.url
        elif hasattr(instance, 'image'):
            url = domain + instance.image.url
        elif hasattr(instance, 'video'):
            url = instance.youtube_link
        else:
            url = domain

        activity_objects.append({
            'type': 'Feature',
            'geometry': None,
            'properties': {
                'hasType': 'MediaFile',
                'name': instance.name,
                'external_url': make_cm_url(external_url),
                'additionalProperties': {
                    'description': instance.description,
                    'url': url
                }
            }
        })

        visibility_details.append({
            'external_url': make_cm_url(external_url),
            'hidden': hidden
        })

        details['project_id'] = contribution.project.id
        details['category_id'] = contribution.category.id
        details['contribution_id'] = contribution.id

    # ###########################
    # FINAL EVENT OBJECT
    # ###########################

    event = {
        'actor': int(uwum_account.id),
        'timestamp': int(round(time.time() * 1000)),
        'activity_type': 'object_%s' % action,
        'activity_objects': activity_objects,
        'visibility_details': visibility_details,
        'details': details
    }

    return event


def send_events(events):
    """Send OnToMap events."""
    cert = get_cert()
    url = settings.ONTOMAP_URLS['EVENTS_URL']

    if events:
        # Always make sure mapings are up-to-date before sending event
        check_mappings()

        data = {
            'event_list': events
        }

        response = request(
            'POST',
            headers=headers,
            url=url,
            cert=cert,
            data=json.dumps(data))

        return response
