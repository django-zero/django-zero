from django.urls import path
from {{cookiecutter.package}}.views import WelcomeView

urlpatterns = [
    path('', WelcomeView.as_view())
]
