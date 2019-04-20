# noinspection PyUnresolvedReferences
import os

from config.settings import *

# This is required so lie server actually serve assets
del STATICFILES_STORAGE

# Test database configuration
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.path.join(BASE_DIR, "db.test.sqlite3")}}
