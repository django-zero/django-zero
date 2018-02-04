import collections
import operator
import os
from functools import reduce

import django_zero


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
        raise RuntimeError('You must run "django-zero install" first, which depends on node.js and yarn.')


def get_env():
    base_path = os.path.dirname(django_zero.__file__)
    return {
        'DJANGO_BASE_DIR': os.getcwd(),
        'DJANGO_ZERO_BASE_DIR': base_path,
        'NODE_PATH': os.path.dirname(base_path),
    }
