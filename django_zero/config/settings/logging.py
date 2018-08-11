# Logging
import logging
import os

import mondrian

LOGGING = {}
LOGGING_CONFIG = None
mondrian.setup(excepthook=True)
logging.getLogger().setLevel(os.getenv("DJANGO_LOG_LEVEL", "INFO"))
