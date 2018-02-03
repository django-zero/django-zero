import collections
import operator
import os
from functools import reduce


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


if __name__ == '__main__':
    l1 = [1, 2, 3]
    l2 = [10, 20, 30]
    l = LazyListFromLists(l1, l2)
    print(list(l))
