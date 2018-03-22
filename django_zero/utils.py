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

    if val.lower().strip() in ('f', 'false', 'n', 'no', '0'):
        return False

    return True


def check_installed():
    env = get_env()

    node_modules_path = os.path.join(env['DJANGO_ZERO_BASE_DIR'], 'node_modules')
    if not os.path.exists(node_modules_path):
        raise UserError(
            'Global node modules are not installed.',
            'Try running:',
            '  $ django-zero install',
        )

    local_node_modules_path = os.path.join(env['DJANGO_BASE_DIR'], 'node_modules')
    if not os.path.exists(local_node_modules_path):
        raise UserError(
            'Project\'s local node modules are not installed.',
            'Try running:',
            '  $ django-zero install',
        )

    webpack_path = os.path.join(local_node_modules_path, '.bin/webpack')
    if not os.path.exists(webpack_path):
        raise UserError(
            'Webpack binary is not available in local node modules directory.',
            'Make sure that `webpack` is listed in your project\'s `package.json` file and run:',
            '  $ django-zero install',
        )


DEV_EXTRA_REQUIRED_MESSAGE = (
    'You need django-zero development tools to use `{cmd}` ("{req}" not found).\n'
    'Try installing the `dev` extra:\n'
    '  $ pip install django-zero[dev]\n'
).strip()

PROD_EXTRA_REQUIRED_MESSAGE = (
    'You need django-zero production tools to use `{cmd}` ("{req}" not found).\n'
    'Try installing the `prod` extra:\n'
    '  $ pip install django-zero[prod]\n'
).strip()


def check_dev_extras(cmd):
    try:
        import cookiecutter
    except ImportError:
        raise UserError(*DEV_EXTRA_REQUIRED_MESSAGE.format(cmd=cmd, req='cookiecutter').split('\n'))

    try:
        import medikit
    except ImportError:
        raise UserError(*DEV_EXTRA_REQUIRED_MESSAGE.format(cmd=cmd, req='medikit').split('\n'))

    try:
        import honcho
    except ImportError:
        raise UserError(*DEV_EXTRA_REQUIRED_MESSAGE.format(cmd=cmd, req='honcho').split('\n'))


def check_prod_extras(cmd):
    try:
        import gunicorn
    except ImportError:
        raise UserError(*PROD_EXTRA_REQUIRED_MESSAGE.format(cmd=cmd, req='gunicorn').split('\n'))


def get_env():
    base_path = os.path.dirname(django_zero.__file__)
    return {
        'DJANGO_BASE_DIR': os.getcwd(),
        'DJANGO_ZERO_BASE_DIR': base_path,
        'NODE_PATH': os.path.dirname(base_path),
    }
