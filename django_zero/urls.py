from django.conf import settings
from django.urls import include, path

urlpatterns = []

for app in settings.INSTALLED_APPS:
    if app.startswith('apps.'):
        urlpatterns.append(path('', include(app + '.urls')))

urlpatterns.append(path('', include('allauth.urls')))

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path(r'__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
