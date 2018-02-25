"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os

import django
import django_zero
from channels.routing import get_default_application

django_zero.configure(os.path.dirname(os.path.dirname(__file__)))
django.setup()

application = get_default_application()
