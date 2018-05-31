import os
import sys

from django_zero.commands import BaseCommand
from django_zero.commands.utils.processes import call_webpack
from django_zero.utils import check_installed, get_env


class DjangoCommand(BaseCommand):
    """Runs the django manage.py script after setting environment."""

    def handle(self, *args):
        check_installed()
        env = get_env()
        # Add CWD and make sure django-zero base path is not in path so we avoid loading its settings instead of user's.
        sys.path = [os.getcwd()] + list(filter(lambda p: p and not p == env['DJANGO_ZERO_BASE_DIR'], sys.path))

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        os.environ.setdefault('DJANGO_BASE_DIR', env.get('DJANGO_BASE_DIR', os.getcwd()))
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


class GunicornCommand(BaseCommand):
    """Serve your project using gunicorn. You must have a valid config/wsgi.py file for this to work."""

    def handle(self, *args):
        try:
            from gunicorn.app.wsgiapp import WSGIApplication
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError('Gunicorn not found. Please install it (pip install gunicorn).') from exc

        _sys_argv_backup, sys.argv = sys.argv, [sys.argv[1], 'config.wsgi', *sys.argv[2:]]
        try:
            WSGIApplication('django-zero %(prog)s [OPTIONS]').run()
        finally:
            sys.argv = _sys_argv_backup


class DaphneCommand(BaseCommand):
    """Serve your project using daphne. You must have a valid config/asgi.py file for this to work."""

    def handle(self, *args):
        from daphne.cli import CommandLineInterface as DaphneCLI

        _sys_argv_backup, sys.argv = sys.argv, [sys.argv[1], 'config.asgi:application', *sys.argv[2:]]
        try:
            DaphneCLI.entrypoint()
        finally:
            sys.argv = _sys_argv_backup


class CeleryCommand(BaseCommand):
    """Runs the celery CLI."""

    def handle(self, *args):
        from celery.__main__ import main as celery_main
        _sys_argv_backup, sys.argv = sys.argv, [' '.join(sys.argv[0:2]), '-A', 'config.celery', *sys.argv[2:]]
        try:
            celery_main()
        finally:
            sys.argv = _sys_argv_backup


class WebpackCommand(BaseCommand):
    """Runs weppack using your project's configuration (in config/webpack.js)."""

    def add_arguments(self, parser):
        parser.add_argument('--production', '--prod', '-p', action='store_true')

    def handle(self, *args, production=False):
        check_installed()
        environ = {
            'NODE_ENV': 'production' if production else 'development'
        }
        return call_webpack(*args, environ=environ)
