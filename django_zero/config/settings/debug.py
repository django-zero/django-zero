from django_zero.utils import get_bool_from_env

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_bool_from_env('DJANGO_DEBUG')