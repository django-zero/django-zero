import os

from django_zero._version import __version__

DEFAULT_DJANGO_SETTINGS_MODULE = 'config.settings'


def configure(base_dir, *, settings_module=DEFAULT_DJANGO_SETTINGS_MODULE):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
    os.environ.setdefault('DJANGO_BASE_DIR', base_dir)


__version__ = __version__
