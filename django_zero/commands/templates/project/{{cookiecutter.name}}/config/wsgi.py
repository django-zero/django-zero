import os

from django.core.wsgi import get_wsgi_application
import django_zero

django_zero.configure(os.path.dirname(os.path.dirname(__file__)))

application = get_wsgi_application()
