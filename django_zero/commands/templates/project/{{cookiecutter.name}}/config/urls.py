from django.contrib import admin

from django_zero.urls import urlpatterns as django_zero_urlpatterns

urlpatterns = [
    # Uncomment for I18n routes, or delete.
    # path('i18n/', include('django.conf.urls.i18n')),
    *django_zero_urlpatterns
]

admin.site.site_header = "Django Zero"
