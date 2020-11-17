import collections
import operator
import os
from functools import reduce

import django_zero
from django_zero.errors import UserError


class LazyListFromLists(collections.Sequence):
    def __init__(self, *lists):
        self._lists = lists

    def __getitem__(self, item):
        i = 0

        while len(self._lists[i]) <= item:
            i += 1
            item -= len(self._lists[i])

        return self._lists[i][item]

    def __iter__(self):
        for l in self._lists:
            yield from l

    def __len__(self):
        return reduce(operator.add, map(len, self._lists), 0)


def get_bool_from_env(var, default=False):
    val = os.environ.get(var, default)

    if not val:
        return False

    if type(val) is bool:
        return val

    if not len(val):
        return False

    if val.lower().strip() in ("f", "false", "n", "no", "0"):
        return False

    return True


def get_list_from_env(name, default=None):
    """Helper to get list from environment."""
    if name not in os.environ:
        return default or []
    return os.environ[name].split(",")


def get_map_from_env(name, default={}):
    """
    Helper to get mapping from environment.
    parses 'first_name:name,email:mail'
    into {'email': 'mail', 'first_name': 'name'}
    """
    if os.environ.get(name):
        return dict(e.split(":") for e in os.environ[name].split(","))
    return {}


def create_directories_or_ignore(*dirs):
    actual_dirs = []

    for _dir in dirs:
        if not os.path.exists(_dir):
            try:
                os.makedirs(_dir)
            except OSError:
                continue
        actual_dirs.append(_dir)

    return actual_dirs


def check_installed():
    from django_zero.config.settings import features

    env = get_env()

    if features.is_webpack_enabled():
        node_modules_path = os.path.join(env["DJANGO_ZERO_BASE_DIR"], "node_modules")
        if not os.path.exists(node_modules_path):
            raise UserError(
                "Django-zero's global node modules are not installed.", "Try running:", "  $ django-zero install"
            )

        local_node_modules_path = os.path.join(env["DJANGO_BASE_DIR"], "node_modules")
        if not os.path.exists(local_node_modules_path):
            raise UserError(
                "Project's local node modules are not installed.", "Try running:", "  $ django-zero install"
            )

        webpack_path = os.path.join(local_node_modules_path, ".bin/webpack-cli")
        if not os.path.exists(webpack_path):
            raise UserError(
                "Webpack CLI binary is not available in local node modules directory.",
                "Make sure that `webpack-cli` is listed in your project's `package.json` file and run:",
                "  $ django-zero install",
            )


DEV_EXTRA_REQUIRED_MESSAGE = (
    'You need django-zero development tools to use `{cmd}` ("{req}" not found).\n'
    "Try installing the `dev` extra:\n"
    "  $ pip install django-zero[dev]\n"
).strip()

PROD_EXTRA_REQUIRED_MESSAGE = (
    'You need django-zero production tools to use `{cmd}` ("{req}" not found).\n'
    "Try installing the `prod` extra:\n"
    "  $ pip install django-zero[prod]\n"
).strip()


def check_dev_extras(cmd):
    try:
        import cookiecutter
    except ImportError:
        raise UserError(*DEV_EXTRA_REQUIRED_MESSAGE.format(cmd=cmd, req="cookiecutter").split("\n"))

    try:
        import medikit
    except ImportError:
        raise UserError(*DEV_EXTRA_REQUIRED_MESSAGE.format(cmd=cmd, req="medikit").split("\n"))

    try:
        import honcho
    except ImportError:
        raise UserError(*DEV_EXTRA_REQUIRED_MESSAGE.format(cmd=cmd, req="honcho").split("\n"))


def check_prod_extras(cmd):
    try:
        import gunicorn
    except ImportError:
        raise UserError(*PROD_EXTRA_REQUIRED_MESSAGE.format(cmd=cmd, req="gunicorn").split("\n"))


def get_env():
    base_path = os.path.dirname(django_zero.__file__)
    return {"DJANGO_BASE_DIR": os.getcwd(), "DJANGO_ZERO_BASE_DIR": base_path, "NODE_PATH": os.path.dirname(base_path)}


def url_for_help(path):
    return "https://django-zero.github.io/" + path.lstrip("/")


def decorated_patterns(*args):
    """
    Enables for the decoration of entire urlpatterns
    with 1...n decorators within a Django urls.py
    instead of
    needing to decorate each View individually 1..n times

    For detailed examples and documentation see:
    http://ddenhartog.github.io/django-urlpattern-decorator/
    """

    decorators, url_patterns = args[0:-1], args[-1]
    decorators = tuple(decorators) if hasattr(decorators, "__iter__") else (decorators,)

    def decorate_url_pattern(decorators, url_pattern):
        if not hasattr(url_pattern, "resolve"):
            return url_pattern
        resolve = getattr(url_pattern, "resolve")

        def decorate_resolve(*args, **kwargs):
            result = resolve(*args, **kwargs)
            if not hasattr(result, "func"):
                return result

            resolve_func = getattr(result, "func")
            for decorator in reversed(decorators):
                resolve_func = decorator(resolve_func)

            setattr(result, "func", resolve_func)
            return result

        setattr(url_pattern, "resolve", decorate_resolve)
        return url_pattern

    return [decorate_url_pattern(decorators, url_pattern) for url_pattern in url_patterns]
