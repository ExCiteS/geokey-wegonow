"""All URLs for the extension."""

from django.conf.urls import url

from geokey_wegovnow import views


urlpatterns = [
    # ###########################
    # PUBLIC API
    # ###########################

    url(r'^api/wegovnow/'
        r'navigation/$',
        views.UWUMNavigationAPIView.as_view(),
        name='api_uwum_navigation'),
]
