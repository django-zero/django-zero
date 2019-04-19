import warnings

from django_zero.config.settings.base import DEBUG
from django_zero.config.settings.features import is_channels_enabled, is_whitenoise_enabled

_debug_only_apps = []
_debug_only_middlewares = []

if DEBUG:
    try:
        import django_extensions

        _debug_only_apps.append("django_extensions")
    except ImportError:
        warnings.warn("Django Extensions are not available, skipping.")

    try:
        import debug_toolbar

        _debug_only_apps.append("debug_toolbar")
        _debug_only_middlewares.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    except ImportError:
        warnings.warn("Django Debug Toolbar is not available, skipping.")

# Applications
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    *(["channels"] if is_channels_enabled() else []),
    "django.contrib.staticfiles",
    *_debug_only_apps,
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]


# Middlewares
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    *(["whitenoise.middleware.WhiteNoiseMiddleware"] if is_whitenoise_enabled() else []),
    *_debug_only_middlewares,
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Urls
ROOT_URLCONF = "django_zero.urls"

# WSGI Application
WSGI_APPLICATION = "config.wsgi.application"

# ASGI Application
if is_channels_enabled():
    ASGI_APPLICATION = "config.routing.application"

# Site
SITE_ID = 1

# Redirect URLs
LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/profile"
ADMIN_URL = "/admin"

__all__ = [
    "ADMIN_URL",
    "INSTALLED_APPS",
    "LOGIN_REDIRECT_URL",
    "LOGIN_URL",
    "MIDDLEWARE",
    "ROOT_URLCONF",
    "SITE_ID",
    "WSGI_APPLICATION",
    *(["ASGI_APPLICATION"] if is_channels_enabled() else []),
]
