# Static files (CSS, JavaScript, Images)

import os

from django_zero.config.settings.features import is_whitenoise_enabled
from django_zero.utils import create_directories_or_ignore

from .base import BASE_DIR, ZERO_DIR

STATICFILES_DIRS = create_directories_or_ignore(
    os.path.join(BASE_DIR, "resources/static"),
    os.path.join(BASE_DIR, ".cache/webpack"),
    os.path.join(ZERO_DIR, "resources/static"),
)

if is_whitenoise_enabled():
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
else:
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = os.environ.get("STATIC_URL", "/static/")

__all__ = ["STATICFILES_DIRS", "STATICFILES_STORAGE", "STATIC_ROOT", "STATIC_URL"]
