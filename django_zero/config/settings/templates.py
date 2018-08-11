import os

from django_zero.config.settings.base import BASE_DIR, ZERO_DIR

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [os.path.join(BASE_DIR, "resources/jinja2"), os.path.join(ZERO_DIR, "resources/jinja2")],
        "APP_DIRS": True,
        "OPTIONS": {"environment": "django_zero.jinja2.environment"},
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "resources/templates"), os.path.join(ZERO_DIR, "resources/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    },
]

__all__ = ["TEMPLATES"]
