"""Logger for OntoMap."""

from allauth.socialaccount.models import SocialAccount

from django.apps import apps
from django.contrib.sites.models import Site
from allauth.socialaccount import app_settings

from geokey.users.models import User
from .base import api_call, created_json, ONTOMAP_URLS, mappingjson

import requests
import time
import string
import json

    
def send_events(event_json):
    """Send events to OntoMap API."""
    event_url = ONTOMAP_URLS['event']
    # uwum_settings = app_settings.PROVIDERS.get('uwum', {})
    # cert_path = uwum_settings['CERT']
    cert_path = get_cert_path()
    try:
        # headers = {'content-type': 'application/json;charset=utf-8'}
        headers = {'content-type': 'application/json'}
        print ("WWWWWWWWwww")
        print ("WWWWWWWWwww")
        print event_url
        print cert_path
        print headers
        print event_json

        print ("WWWWWWWWwww")
        print ("WWWWWWWWwww")
        events_rqst = requests.post(
            event_url,
            headers=headers,
            data=event_json,
            cert=cert_path
        )
        print "response", events_rqst.content
    except Exception as e:
        print "error is", e
        return


def send_mapping():
    """Send mappings to OntoMap API."""
    mapping_url = ONTOMAP_URLS['mapping']
    # uwum_settings = app_settings.PROVIDERS.get('uwum', {})
    # cert_path = uwum_settings['CERT']
    cert_path = get_cert_path()

    try:
        headers = {'content-type': 'application/json;charset=utf-8'}
        # headers = {'content-type': 'application/json'}
        mapping_rqst = requests.post(
            mapping_url,
            headers=headers,
            data=json.loads(mappingjson),
            cert=cert_path
        )
        print "MAPPING RESPONSE", mapping_rqst.content
        print "MAPPING RESPONSE", mapping_rqst.status_code
    except Exception as e:
        print "error is", e


def get_events():
    """Get the events from OntoMap API."""
    event_get_url = ONTOMAP_URLS['event']
    uwum_settings = app_settings.PROVIDERS.get('uwum', {})
    cert_path = uwum_settings['CERT']

    try:
        carabassa = requests.get(event_get_url, cert=cert_path)
        print "response", carabassa.content
    except Exception as e:
        print "error is", e


def replace_url(instance, class_name):
    """Replace the urls on the json event."""

    domain = "http://127.0.0.1:8000"
    # domain = Site.objects.get_current().domain  <---- Domain get from Site
    replacements = {
        '$project_id$': instance.project['id']
    }
    if class_name == 'Observation' or class_name == 'Comments':
        replacements['$contrib_id$'] = instance.observation['id']
    elif class_name == 'MediaFile':
        replacements['$media_id']

    if class_name == "Category":
        replacements['$category_id$'] = instance.category['id']

    if class_name == "Field":
        replacements['$category_id$'] = instance.category['id']
        replacements['$field_id$'] = instance.field['id']
    print("888888888888888",class_name)
    url = api_call[class_name]
    for src, target in replacements.iteritems():
        url = string.replace(url, src, str(target))
    return domain + url


def create_event(instance, class_name, action):
    """Create the json to replace the event."""
    replacements = {
        '$uwum_user_id$': SocialAccount.objects.get(
            provider='uwum',
            user=User.objects.get(id=instance.user['id'])
        ).id,
        '$activity_type$': 'object_' + action,
        '$timestamp$': int(time.time()),
        '$external_url$': replace_url(instance, class_name),
        '$hidden$': "false"

    }

    #if action == 'updated' or 'created':
    #    print "we get inside updated"
    #    replacements['$additional_prop$'] = get_additional_properties(
    #        instance,
    #        class_name
    #    )
    #else:
    replacements['$additional_prop$'] = {}

    if class_name != 'Observation':
        # Only geometry exists when it Observation -- Location
        replacements['$geometry$'] = "null"
        # replacements['$geometry$'] = """{
        #                 "type": "Point",
        #                 "coordinates": [
        #                     7.70077228546143,
        #                     45.0734069562204
        #                 ]
        #             }"""

        replacements['$hasType$'] = class_name
    else:
        replacements['$geometry$'] = instance.location.geometry
        replacements['$hasType$'] = "AtomicThing"
        if instance.status != "active":
            replacements["$hidden$"] = "false"

    event = created_json
    for src, target in replacements.iteritems():
        event = string.replace(event, src, str(target))

    return event


def get_cert_path():
    """Get the certificate path."""
    uwum_settings = app_settings.PROVIDERS.get('uwum', {})
    cert_path = uwum_settings['CERT']

    return cert_path


def get_additional_properties(instance, class_name):
    """Get additional properties to added to the event.

    Basically makes a call to GeoKey api object and append the information
    for the additionalProperties key on the json event for th OntoMap API call.
    """
    cert = get_cert_path()
    print ("cert is ", cert)
    try:
        print ("sssssssssssssss ", class_name)
        print "URL", replace_url(instance, class_name)
        response = requests.get(replace_url(instance, class_name), cert=cert)
        print "response.status_code", response.status_code
        if response.status_code == 200:
            print "CERDERA", response.content
            return response.content
        else:
            return
    except:
        return




# get_events()
# send_mapping()
