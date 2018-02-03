from django.apps import AppConfig


class {{ cookiecutter.name | camelcase }}Config(AppConfig):
    name = '{{ cookiecutter.name }}'
