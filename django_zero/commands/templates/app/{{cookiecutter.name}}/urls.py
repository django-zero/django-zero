from django.urls import path

from apps.{{ cookiecutter.name }}.views import WelcomeView

urlpatterns = [
    path('', WelcomeView.as_view())
]
