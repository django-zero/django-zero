# noinspection PyUnresolvedReferences
from django_zero.config.settings import *

SECRET_KEY = 's3cr3t'

INSTALLED_APPS += [
    # Add your own applications there.
]

# Add demo urls.
# Remove the line to disable.
ZERO_ENABLE_DEMO = True
