from django.apps import AppConfig


class {{ cookiecutter.app | camelcase }}Config(AppConfig):
    name = '{{ cookiecutter.app }}'
