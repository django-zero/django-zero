import os
import sys

import django_zero
from django_zero.commands import AbstractSubcommand
from django_zero.commands.utils.processes import call_webpack
from django_zero.config.settings.features import is_celery_enabled
from django_zero.utils import check_installed, get_env


class DjangoCommand(AbstractSubcommand):
    """Runs the django manage.py script after setting environment."""

    def handle(self, *args):
        # This is a hack to ensure environment tuning is imported. Probably something more solid should be thought
        # about.
        __import__("config")

        check_installed()
        env = get_env()
        # Add CWD and make sure django-zero base path is not in path so we avoid loading its settings instead of user's.
        sys.path = list(
            dict.fromkeys([os.getcwd()] + list(filter(lambda p: p and not p == env["DJANGO_ZERO_BASE_DIR"], sys.path)))
        )

        django_zero.configure(env.get("DJANGO_BASE_DIR", os.getcwd()))
        os.environ.setdefault("DJANGO_DEBUG", "true")

        try:
            from django.core.management import execute_from_command_line
        except ImportError as exc:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc
        return execute_from_command_line(["django-zero manage"] + list(args))


class GunicornCommand(AbstractSubcommand):
    """Serve your project using gunicorn. You must have a valid config/wsgi.py file for this to work."""

    def handle(self, *args):
        try:
            from gunicorn.app.wsgiapp import WSGIApplication
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError("Gunicorn not found. Please install it (pip install gunicorn).") from exc

        _sys_argv_backup, sys.argv = sys.argv, [sys.argv[1], "config.wsgi", *sys.argv[2:]]
        try:
            WSGIApplication("django-zero %(prog)s [OPTIONS]").run()
        finally:
            sys.argv = _sys_argv_backup


class DaphneCommand(AbstractSubcommand):
    """Serve your project using daphne. You must have a valid config/asgi.py file for this to work."""

    def handle(self, *args):
        from daphne.cli import CommandLineInterface as DaphneCLI

        _sys_argv_backup, sys.argv = sys.argv, [sys.argv[1], "config.asgi:application", *sys.argv[2:]]
        try:
            DaphneCLI.entrypoint()
        finally:
            sys.argv = _sys_argv_backup


class CeleryCommand(AbstractSubcommand):
    """Runs the celery CLI."""

    @classmethod
    def is_enabled(cls):
        return is_celery_enabled()

    def handle(self, *args):
        from celery.__main__ import main as celery_main

        _sys_argv_backup, sys.argv = sys.argv, [" ".join(sys.argv[0:2]), "-A", "config.celery", *sys.argv[2:]]
        try:
            celery_main()
        finally:
            sys.argv = _sys_argv_backup


class WebpackCommand(AbstractSubcommand):
    """Runs weppack using your project's configuration (in config/webpack.js)."""

    webpack_command = "webpack-cli"

    def add_arguments(self, parser):
        parser.add_argument("--production", "--prod", "-p", action="store_true")

    def get_environ(self, production=False):
        return {"NODE_ENV": "production" if production else "development"}

    def handle(self, *args, **kwargs):
        check_installed()
        return call_webpack(*args, command=self.webpack_command, environ=self.get_environ(**kwargs))


class WebpackDevServerCommand(WebpackCommand):
    webpack_command = "webpack-dev-server"

    def add_arguments(self, parser):
        super(WebpackDevServerCommand, self).add_arguments(parser)
        dev_server = parser.add_mutually_exclusive_group(required=False)
        dev_server.add_argument("--hot", action="store_true")
        dev_server.add_argument("--hot-only", action="store_true")

    def get_environ(self, hot=False, hot_only=False, production=False):
        if production and (hot or hot_only):
            raise RuntimeError("Cannot run webpack-dev-server while in production mode.")
        environ = super(WebpackDevServerCommand, self).get_environ(production=production)
        if hot:
            environ["WEBPACK_DEV_SERVER"] = "hot"
        elif hot_only:
            environ["WEBPACK_DEV_SERVER"] = "hot-only"
        return environ
