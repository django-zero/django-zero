import logging

from django.conf import settings
from django.urls import include, path

from django_zero import views

urlpatterns = []

for app in settings.INSTALLED_APPS:
    if app.startswith('apps.'):
        urlpatterns.append(path('', include(app + '.urls')))

urlpatterns.append(path('', include('allauth.urls')))

if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns = [
            path(r'__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError as exc:
        logging.getLogger(__name__).exception('Could not import debug_toolbar, skipping.')

if settings.DEBUG and settings.ZERO_ENABLE_DEMO:
    # Default example views
    urlpatterns.append(path('', views.example_feature_list_view, name='example_feature_list'))
    urlpatterns.append(path('<slug>', views.example_feature_detail_view, name='example_feature_detail'))
