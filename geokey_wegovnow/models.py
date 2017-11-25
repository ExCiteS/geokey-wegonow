"""All models for the WeGovNow extension."""

import os

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from geokey.core.models import get_class_name, cross_check_fields

from geokey_wegovnow.base import LOG_MODELS, WATCHED_FIELDS
from geokey_wegovnow.logger import make_event, send_events


@receiver(pre_save)
def log_on_pre_save(sender, instance, **kwargs):
    """Init events, make event when instance is updated/deleted."""
    if 'TRAVIS' not in os.environ:
        events = []

        instance._class_name = get_class_name(sender)
        instance._logged = False

        if sender.__name__ in LOG_MODELS:
            if instance.status == 'deleted':
                # If instance status changes to "deleted" - make event "deleted"
                events.append(make_event(
                    instance._class_name,
                    instance,
                    'deleted'))
                instance._logged = True
            else:
                try:
                    # Old instance is needed for checking changed fields
                    old_instance = sender.objects.get(pk=instance.pk)

                    checked_fields = cross_check_fields(instance, old_instance)
                    changed_fields = [
                        x for x in checked_fields
                        if x.get('field') in WATCHED_FIELDS
                    ]

                    if any(changed_fields):
                        # If watched fields changed - make event "updated"
                        events.append(make_event(
                            instance._class_name,
                            instance,
                            'updated'))
                        instance._logged = True
                except sender.DoesNotExist:
                    pass

        # Do not send events just yet - save in instance for now
        instance._events = events


@receiver(post_save)
def log_on_post_save(sender, instance, created, **kwargs):
    """Finalise events, make event when instance is created."""
    if 'TRAVIS' not in os.environ:
        if created and not instance._logged and sender.__name__ in LOG_MODELS:
            # If nothing logged and instance is created - make event "created"
            instance._events.append(make_event(
                instance._class_name,
                instance,
                'created'))

        # Now send events
        send_events(instance._events)
