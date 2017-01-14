from django.conf.urls import url
from .views import (
    ChangeLikedFundView
)


urlpatterns = [
    url(r'^like/fund/$', ChangeLikedFundView.as_view(), name='likedfund_change'),
]
