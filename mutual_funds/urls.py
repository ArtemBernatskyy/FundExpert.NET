from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('mutual_funds.landing.urls', namespace='landing')),
    url(r'^finance/', include('mutual_funds.finance.urls', namespace='finance')),
    url(r'^auth/', include('mutual_funds.registration.backends.default.urls')),
    url(r'^accounts/', include('mutual_funds.accounts.urls', namespace='accounts')),
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^api/funds/', include('mutual_funds.finance.api.urls', namespace='fund-api')),
    url(r'^api/accounts/', include('mutual_funds.accounts.api.urls', namespace='account-api')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ]
