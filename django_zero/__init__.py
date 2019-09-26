import logging
import os

from django_zero._version import __version__

logger = logging.getLogger(__name__)

DEFAULT_DJANGO_SETTINGS_MODULE = "config.settings"


def configure(base_dir, *, settings_module=DEFAULT_DJANGO_SETTINGS_MODULE):
    logger.debug("Base dir: %s", base_dir)
    os.environ.setdefault("DJANGO_BASE_DIR", base_dir)
    logger.debug("Settings module: %s", settings_module)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)


__version__ = __version__
