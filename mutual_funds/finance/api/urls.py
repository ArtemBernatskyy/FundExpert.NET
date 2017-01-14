from django.conf.urls import url

from .views import (
    FundDetailAPIView, FundListAPIView
)


urlpatterns = [
    url(r'^$', FundListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', FundDetailAPIView.as_view(), name='detail'),
]
