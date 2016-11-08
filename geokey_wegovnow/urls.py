"""All URLs for the extension."""

from django.conf.urls import include, url

from rest_framework.urlpatterns import format_suffix_patterns

from geokey_wegovnow import views


# ###########################
# ADMIN VIEWS
# ###########################

adminpatterns = [
    url(r'^admin/profile/settings/$',
        views.UWUMProfileSettingsView.as_view(),
        name='uwum_profile_settings'),
]

# ###########################
# PUBLIC API
# ###########################

apipatterns = [
    url(r'^api/wegovnow/'
        r'navigation/$',
        views.UWUMNavigationAPIView.as_view(),
        name='api_uwum_navigation'),
]
apipatterns = format_suffix_patterns(apipatterns, allowed=['json', 'raw_html'])

# ###########################
# COMBINED URLS
# ###########################

urlpatterns = [
    url(
        r'^', include(adminpatterns)),
    url(
        r'^', include(apipatterns)),
]
