"""Custom WeGovNow template tags."""

from django import template


register = template.Library()


@register.filter()
def exclude_uwum_app(apps):
    """Exclude UWUM app."""
    apps_without_uwum = []

    for app in apps:
        if app.provider.id != 'uwum':
            apps_without_uwum.append(app)

    return apps_without_uwum


@register.filter()
def exclude_uwum_accounts(accounts):
    """Exclude UWUM accounts."""
    return accounts.exclude(provider='uwum')


@register.filter()
def is_twitter(socialinteraction):
    """Exclude UWUM accounts."""
    value = False
    for sa in socialinteraction.socialaccounts.all():
        if sa.provider == 'twitter':
            value = True
    return value