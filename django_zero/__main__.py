import argparse
import logging
import os
import shutil
import subprocess
import sys

import django_zero
from django_zero.commands import BaseCommand
from django_zero.commands.init import InitCommand
from django_zero.commands.start import StartCommand
from django_zero.processes import call_webpack
from django_zero.utils import check_installed, get_env

import mondrian


def handle_webpack(*args):
    check_installed()
    return call_webpack(*args)


def handle_gunicorn(*args):
    from gunicorn.app.wsgiapp import WSGIApplication

    _sys_argv_backup, sys.argv = sys.argv, [sys.argv[1], 'config.wsgi', *sys.argv[2:]]
    try:
        WSGIApplication('django-zero %(prog)s [OPTIONS]').run()
    finally:
        sys.argv = _sys_argv_backup


def handle_manage(*args):
    check_installed()
    env = get_env()
    # Add CWD and make sure django-zero base path is not in path so we avoid loading its settings instead of user's.
    sys.path = [os.getcwd()] + list(filter(lambda p: p and not p == env['DJANGO_ZERO_BASE_DIR'], sys.path))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    os.environ.setdefault('DJANGO_BASE_DIR', env['DJANGO_BASE_DIR'])
    os.environ.setdefault('DJANGO_DEBUG', 'true')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    return execute_from_command_line(['django-zero manage'] + list(args))


def handle_install():
    env = get_env()
    subprocess.call('yarn install', cwd=env['DJANGO_ZERO_BASE_DIR'], shell=True)


def handle_uninstall():
    check_installed()
    env = get_env()
    shutil.rmtree(os.path.join(env['DJANGO_ZERO_BASE_DIR'], 'node_modules'))


def handle_path():
    print(os.path.dirname(django_zero.__file__))


commands = {
    'init': InitCommand,
    'gunicorn': handle_gunicorn,
    'manage': handle_manage,
    'path': handle_path,
    'start': StartCommand,
    'webpack': handle_webpack,
    'install': handle_install,
    'uninstall': handle_uninstall,
}


def main():
    mondrian.setup(excepthook=True)

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    for command, command_handler in commands.items():
        subparser = subparsers.add_parser(command)
        if isinstance(command_handler, type) and issubclass(command_handler, BaseCommand):
            command_instance = command_handler()
            command_instance.add_arguments(subparser)
            subparser.set_defaults(handler=command_instance.handle)
        else:
            subparser.set_defaults(handler=command_handler)

    options, rest = parser.parse_known_args()
    options = options.__dict__

    options.pop('command')
    debug = options.pop('debug')
    handler = options.pop('handler')

    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

    return handler(*rest, **options)


if __name__ == '__main__':
    retval = main()

    if retval:
        sys.exit(int(retval))
