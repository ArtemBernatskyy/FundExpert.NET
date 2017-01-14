from django.conf.urls import url

from .views import (
    MainPageView, NewsDetailView, FAQView, AboutView
)

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='main_page'),
    url(r'^faq/$', FAQView.as_view(), name='faq'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^post/(?P<slug>[-\w]+)/$', NewsDetailView.as_view(), name='detail'),
]
