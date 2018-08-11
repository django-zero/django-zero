# noinspection PyUnresolvedReferences
from django_zero.config.settings import *

# Django secret. Change to some random string.
# One way to generate one: openssl rand -base64 32
SECRET_KEY = "s3cr3t"

INSTALLED_APPS += [
    # Add your own applications there.
]

# Use the local routing table.
ROOT_URLCONF = "config.urls"

# Add demo urls (remove the line to disable).
ZERO_ENABLE_DEMO = True
