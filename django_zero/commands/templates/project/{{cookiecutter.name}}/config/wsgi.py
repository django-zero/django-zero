"""
WSGI entrypoint. Configures Django and then runs the application
defined in the WSGI_APPLICATION setting.
"""

import os

import django_zero
from django.core.wsgi import get_wsgi_application

django_zero.configure(os.path.dirname(os.path.dirname(__file__)))

application = get_wsgi_application()
