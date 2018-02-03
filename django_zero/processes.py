import os

from honcho.manager import Manager


def create_honcho_manager(printer=None, **kwargs):
    env = {
        **os.environ,
        **kwargs.pop('env', {}),
        'PYTHONUNBUFFERED': '1',
    }
    m = Manager(printer=printer)
    m.add_process('server', 'python -m django_zero manage runserver', env=env)
    m.add_process('assets', 'python -m django_zero webpack --watch --colors', env=env)
    return m
