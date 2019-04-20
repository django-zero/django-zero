from django_zero.config.settings.base import *
from django_zero.config.settings.base import __all__ as _all_base
from django_zero.config.settings.features import is_channels_enabled
from django_zero.utils import get_bool_from_env

from .authentication import *
from .authentication import __all__ as _all_authentication
from .databases import *
from .databases import __all__ as _all_databases
from .django import *
from .django import __all__ as _all_django
from .i18n import *
from .i18n import __all__ as _all_i18n
from .security import *
from .security import __all__ as _all_security
from .staticfiles import *
from .staticfiles import __all__ as _all_staticfiles
from .templates import *
from .templates import __all__ as _all_templates

# Django Zero settings
ZERO_ENABLE_DEMO = get_bool_from_env("ENABLE_DEMO", default=False)
ZERO_ENABLE_EXPERIMENTS = get_bool_from_env("ENABLE_EXPERIMENTS", default=False)

__all__ = (
    _all_base
    + _all_authentication
    + _all_databases
    + _all_django
    + _all_i18n
    + _all_security
    + _all_staticfiles
    + _all_templates
    + ["ZERO_ENABLE_DEMO", "ZERO_ENABLE_EXPERIMENTS"]
)
