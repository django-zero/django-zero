# noinspection PyUnresolvedReferences
import os
from config.settings import *

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.path.join(BASE_DIR, "db.test.sqlite3")}}
