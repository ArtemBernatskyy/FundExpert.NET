from django.conf.urls import url

from .views import (
    MutualFundsRankingView, MSRatingView, SectorsRankingView,
    FundDetailView, SectorDetailView
)


urlpatterns = [
    url(r'^ms_rating/$', MSRatingView.as_view(), name='ms_rating'),
    url(r'^mf_ranking/$', MutualFundsRankingView.as_view(), name='mf_ranking'),
    url(r'^sectors_ranking/$', SectorsRankingView.as_view(), name='sectors_ranking'),
    url(r'^fund/(?P<slug>[-\w]+)/$', FundDetailView.as_view(), name='fund_detail'),
    url(r'^sector/(?P<slug>[-\w]+)/$', SectorDetailView.as_view(), name='sector_detail'),
]
