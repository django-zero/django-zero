import argparse
import logging
import re
from sys import exc_info

import mondrian
from django_zero.commands.base import BaseCommand
from django_zero.commands.create import CreateCommand
from django_zero.commands.delegates import CeleryCommand, DaphneCommand, GunicornCommand, DjangoCommand, WebpackCommand
from django_zero.commands.lifecycle import StartCommand, InstallCommand, PathCommand, UninstallCommand
from django_zero.errors import UserError
from mondrian import term

commands = {
    'celery': CeleryCommand,
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
    parser.add_argument('--debug', '-D', action='store_true')

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

    try:
        return handler(*rest, **options)
    except UserError as exc:
        SPACES = 2
        w = term.white
        prefix = w('║' + ' ' * (SPACES - 1))
        suffix = w(' ' * (SPACES - 1) + '║')

        pre_re = re.compile('([^`]*)`([^`]*)`([^`]*)')

        def format_arg(arg):
            length = len(pre_re.sub('\\1\\2\\3', arg))

            arg = pre_re.sub(w('\\1') + term.bold('\\2') + w('\\3'), arg)
            arg = re.sub('^  \$ (.*)', term.lightblack('  $ ') + term.reset('\\1'), arg)

            return (arg, length)

        def f(*args):
            return ''.join(args)

        term_width, term_height = term.get_size()
        line_length = min(80, term_width)
        for arg in exc.args:
            line_length = max(min(line_length, len(arg) + 2 * SPACES), 120)

        print(f(w('╔' + '═' * (line_length - 2) + '╗')))
        for i, arg in enumerate(exc.args):

            if i == 1:
                print(f(
                    prefix,
                    ' ' * (line_length - 2 * SPACES),
                    suffix,
                ))

            arg_formatted, arg_length = format_arg(arg)
            if not i:
                # first line
                print(
                    f(
                        prefix,
                        term.red_bg(term.bold(' ' + type(exc).__name__ + ' ')),
                        ' ',
                        w(arg_formatted),
                        ' ' * (line_length - (arg_length + 3 + len(type(exc).__name__) + 2 * SPACES)),
                        suffix,
                    )
                )
            else:
                # other lines
                print(f(prefix, arg_formatted + ' ' * (line_length - arg_length - 2 * SPACES), suffix))

        print(f(w('╚' + '═' * (line_length - 2) + '╝')))

        logging.getLogger().debug('This error was caused by the following exception chain.', exc_info=exc_info())
