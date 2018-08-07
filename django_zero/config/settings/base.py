import os

from django_zero.utils import get_bool_from_env

if os.environ.get("DJANGO_BASE_DIR"):
    BASE_DIR = os.environ.get("DJANGO_BASE_DIR")
else:
    BASE_DIR = os.getcwd()
    while not os.path.exists(os.path.join(BASE_DIR, "setup.py")):
        BASE_DIR = os.path.dirname(BASE_DIR).rstrip("/")
        if not len(BASE_DIR):
            raise OSError(
                "Could not find django zero project base directory form cwd, please provide a DJANGO_BASE_DIR value (in env)."
            )

ZERO_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_bool_from_env("DJANGO_DEBUG")

__all__ = ["DEBUG", "BASE_DIR", "ZERO_DIR"]
