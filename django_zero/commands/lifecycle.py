import os
import shutil
import subprocess

import django_zero
from django_zero.commands import BaseCommand
from django_zero.commands.utils.processes import call_webpack, call_manage, create_honcho_manager
from django_zero.utils import get_env, check_installed


class StartCommand(BaseCommand):
    """Starts all processes using honcho, after calling eventual prerequisites."""

    def add_arguments(self, parser):
        parser.add_argument('--prod', '-p', action='store_true')

    def handle(self, *, prod=False):
        if prod:
            call_webpack('-p')
            call_manage('collectstatic', '--noinput')
            m = create_honcho_manager(mode='prod')
        else:
            check_installed()
            m = create_honcho_manager(mode='dev', environ={'DJANGO_DEBUG': '1'})

        m.loop()
        return m.returncode


class InstallCommand(BaseCommand):
    """Runs "yarn install" within the django-zero package, to make shared node dependencies available."""

    def handle(self):
        env = get_env()
        subprocess.call('yarn install', cwd=env['DJANGO_ZERO_BASE_DIR'], shell=True)


class UninstallCommand(BaseCommand):
    """Removes the "node_modules" directory within django-zero package."""

    def handle(self):
        check_installed()
        env = get_env()
        shutil.rmtree(os.path.join(env['DJANGO_ZERO_BASE_DIR'], 'node_modules'))


class PathCommand(BaseCommand):
    """Shows the path of django-zero package."""

    def handle(self):
        print(os.path.dirname(django_zero.__file__))
