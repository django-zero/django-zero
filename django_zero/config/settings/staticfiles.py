# Static files (CSS, JavaScript, Images)

import os

from .base import BASE_DIR, ZERO_DIR

STATIC_URL = os.environ.get('STATIC_URL', '/static/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'resources/static'),
    os.path.join(BASE_DIR, '.cache/webpack'),
    os.path.join(ZERO_DIR, 'resources/static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Let's make sure all those dirs exist.
for _dir in STATICFILES_DIRS:
    if not os.path.exists(_dir):
        try:
            os.makedirs(_dir)
        except OSError:
            STATICFILES_DIRS.remove(_dir)

__all__ = [
    'STATICFILES_DIRS',
    'STATIC_ROOT',
    'STATIC_URL',
]
