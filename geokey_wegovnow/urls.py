"""All URLs for the extension."""

from django.conf.urls import url

from geokey_wegovnow import views


urlpatterns = [
    # ###########################
    # ADMIN VIEWS
    # ###########################

    url(r'^admin/profile/settings/$',
        views.UWUMProfileSettingsView.as_view(),
        name='uwum_profile_settings'),

    # ###########################
    # PUBLIC API
    # ###########################

    url(r'^api/wegovnow/'
        r'navigation/$',
        views.UWUMNavigationAPIView.as_view(),
        name='api_uwum_navigation'),
]
