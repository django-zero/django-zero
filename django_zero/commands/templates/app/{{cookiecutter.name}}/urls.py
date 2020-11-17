from apps.{{cookiecutter.name}}.views import WelcomeView
from django.urls import path

urlpatterns = [
    path('', WelcomeView.as_view())
]
