import logging
import os

import mondrian
from django_zero.config import features
from django_zero.utils import get_bool_from_env

# Directories
BASE_DIR = os.environ.get('DJANGO_BASE_DIR', os.getcwd())
ZERO_DIR = os.path.dirname(os.path.dirname(__file__))

# Django Zero settings
ZERO_ENABLE_DEMO = get_bool_from_env('ENABLE_DEMO', default=False)
ZERO_ENABLE_EXPERIMENTS = get_bool_from_env('ENABLE_EXPERIMENTS', default=False)

# Feature Flags
_is_celery_enabled = features.is_celery_enabled()
_is_channels_enabled = features.is_channels_enabled()
_is_whitenoise_enabled = features.is_whitenoise_enabled()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = None

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_bool_from_env('DJANGO_DEBUG')
_debug_only_apps = []
_debug_only_middlewares = []
if DEBUG:
    try:
        import django_extensions

        _debug_only_apps.append('django_extensions')
    except ImportError:
        pass

    try:
        import debug_toolbar

        _debug_only_apps.append('debug_toolbar')
        _debug_only_middlewares.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    except ImportError:
        pass

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
INTERNAL_IPS = ['127.0.0.1']

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    *(['channels'] if _is_channels_enabled else []),
    'django.contrib.staticfiles',
    *_debug_only_apps,
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    *(['whitenoise.middleware.WhiteNoiseMiddleware'] if _is_whitenoise_enabled else []),
    *_debug_only_middlewares,
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Urls
ROOT_URLCONF = 'django_zero.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            os.path.join(BASE_DIR, 'resources/jinja2'),
            os.path.join(ZERO_DIR, 'resources/jinja2'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'django_zero.jinja2.environment'
        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'resources/templates'),
            os.path.join(ZERO_DIR, 'resources/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
if _is_channels_enabled:
    ASGI_APPLICATION = 'config.routing.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
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

# Site

SITE_ID = 1

# Logging
LOGGING = {}
LOGGING_CONFIG = None
mondrian.setup(excepthook=True)
logging.getLogger().setLevel(os.getenv('DJANGO_LOG_LEVEL', 'INFO'))

# Authentication
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_FORMS = {
    'login': 'django_zero.auth.forms.LoginForm',
    'reset_password': 'django_zero.auth.forms.ResetPasswordForm',
    'signup': 'django_zero.auth.forms.SignupForm',
}

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/profile'
ADMIN_URL = '/admin'
