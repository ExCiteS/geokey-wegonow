"""All URLs for the extension."""

from django.conf.urls import url

from geokey_wegovnow import views


urlpatterns = [
    # ###########################
    # PUBLIC API
    # ###########################

    url(r'^api/wegovnow/'
        r'navigation/$',
        views.NavigationAPIView.as_view(),
        name='api_navigation'),
]
