"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os

import django
from channels.routing import get_default_application

import django_zero

django_zero.configure(os.path.dirname(os.path.dirname(__file__)))
django.setup()

application = get_default_application()
