from django.conf.urls import url

from .views import (
    ProfileDetailView, ProfileUpdateView
)


urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/$', ProfileDetailView.as_view(), name='profile_detail'),
    url(r'^(?P<slug>[-\w]+)/update/$', ProfileUpdateView.as_view(), name='profile_update'),
]
