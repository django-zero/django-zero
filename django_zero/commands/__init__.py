import argparse
import logging

import mondrian

from django_zero.commands.base import BaseCommand
from django_zero.commands.create import CreateCommand
from django_zero.commands.delegates import DaphneCommand, GunicornCommand, DjangoCommand, WebpackCommand
from django_zero.commands.lifecycle import StartCommand, InstallCommand, PathCommand, UninstallCommand

commands = {
    'create': CreateCommand,
    'daphne': DaphneCommand,
    'gunicorn': GunicornCommand,
    'install': InstallCommand,
    'manage': DjangoCommand,
    'path': PathCommand,
    'start': StartCommand,
    'uninstall': UninstallCommand,
    'webpack': WebpackCommand,
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
