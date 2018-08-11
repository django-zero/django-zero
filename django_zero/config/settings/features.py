from functools import lru_cache

from django_zero.utils import get_bool_from_env


@lru_cache()
def is_celery_enabled():
    return get_bool_from_env("ENABLE_CELERY", default=False)


@lru_cache()
def is_channels_enabled():
    return get_bool_from_env("ENABLE_CHANNELS", default=False)


@lru_cache()
def is_whitenoise_enabled():
    return get_bool_from_env("ENABLE_WHITENOISE", default=True)
