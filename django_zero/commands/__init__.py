import argparse
import logging
import os
import sys

import mondrian
from mondrian import humanizer

from django_zero.commands.base import AbstractSubcommand
from django_zero.commands.create import CreateCommand
from django_zero.commands.delegates import (
    CeleryCommand, DaphneCommand, DjangoCommand, GunicornCommand, WebpackCommand, WebpackDevServerCommand
)
from django_zero.commands.lifecycle import InstallCommand, PathCommand, StartCommand, UninstallCommand

logger = logging.getLogger(__name__)

commands = {
    "celery": CeleryCommand,
    "create": CreateCommand,
    "daphne": DaphneCommand,
    "gunicorn": GunicornCommand,
    "install": InstallCommand,
    "manage": DjangoCommand,
    "path": PathCommand,
    "start": StartCommand,
    "uninstall": UninstallCommand,
    "webpack": WebpackCommand,
    "webpack-dev-server": WebpackDevServerCommand,
}


def main():
    mondrian.setup(excepthook=True)

    sys.path = list(dict.fromkeys([os.getcwd(), *sys.path]))
    try:
        __import__("config")
    except ImportError:
        pass

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", "-D", action="store_true")

    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    for command, CommandType in commands.items():
        if CommandType.is_enabled():
            subparser = subparsers.add_parser(command)
            command_instance = CommandType()
            command_instance.add_arguments(subparser)
            subparser.set_defaults(handler=command_instance.handle)

    options, rest = parser.parse_known_args()
    options = options.__dict__

    options.pop("command")
    debug = options.pop("debug")
    handler = options.pop("handler")

    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger().debug("Logging level set to DEBUG")

    try:
        with humanizer.humanize():
            return handler(*rest, **options)
    except Exception:
        return 70
