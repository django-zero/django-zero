import os
import shutil
import subprocess

import django_zero
from django_zero.commands import BaseCommand
from django_zero.commands.utils.processes import call_manage, call_webpack, create_honcho_manager
from django_zero.utils import check_dev_extras, check_installed, check_prod_extras, get_env
from mondrian import humanizer, term


class BaseLifecycleCommand(BaseCommand):
    """
    Contains logic for all lifecycle-related commands.

    Abstract (does not implement `handle()`).

    """

    def execute(self, command, *, cwd, shell=True):
        self.logger.info(term.bold('>>> %s') + ' ' + term.lightblack('(in %s)'), command, cwd)

        retval = subprocess.call(command, cwd=cwd, shell=shell)

        if retval:
            self.logger.error(term.red(term.bold('... Failure.')))
            raise RuntimeError('"{}" returned {}.'.format(command, retval))
        else:
            self.logger.info(term.green(term.bold('... Success.')))


class StartCommand(BaseLifecycleCommand):
    """Starts all processes using honcho, after calling eventual prerequisites."""

    def add_arguments(self, parser):
        parser.add_argument("--prod", "-p", action="store_true")

    @humanizer.humanize()
    def handle(self, *, prod=False):
        cmd = "django-zero start"
        check_dev_extras(cmd)

        if prod:
            check_prod_extras(cmd)
            call_webpack("-p")
            call_manage("collectstatic", "--noinput")
            m = create_honcho_manager(mode="prod")
        else:
            check_installed()
            m = create_honcho_manager(mode="dev", environ={"DJANGO_DEBUG": "1"})

        m.loop()
        return m.returncode


class InstallCommand(BaseLifecycleCommand):
    """Runs "yarn install" within the django-zero package, to make shared node dependencies available."""

    def add_arguments(self, parser):
        parser.add_argument('--dev', action='store_const', const='dev', dest='extra')

    @humanizer.humanize()
    def handle(self, extra=None):
        env = get_env()

        zero_dir = env["DJANGO_ZERO_BASE_DIR"]
        project_dir = env["DJANGO_BASE_DIR"]

        self.execute("pip install --quiet -e .{extra}".format(extra='[' + extra + ']' if extra else ''),
                     cwd=project_dir)
        self.execute("yarn install --silent", cwd=zero_dir)
        self.execute("yarn install --silent", cwd=project_dir)


        print(humanizer.Success(
            'Project was installed successfully.',
            "Eventually run migrations, then spawn a dev server:",
            "",
            "  $ `django-zero manage migrate`",
            "  $ `django-zero start`",
        ))


class UninstallCommand(BaseLifecycleCommand):
    """Removes the "node_modules" directory within django-zero package."""

    @humanizer.humanize()
    def handle(self):
        check_installed()
        env = get_env()
        shutil.rmtree(os.path.join(env["DJANGO_ZERO_BASE_DIR"], "node_modules"))


class PathCommand(BaseLifecycleCommand):
    """Shows the path of django-zero package."""

    @humanizer.humanize()
    def handle(self):
        print(os.path.dirname(django_zero.__file__))
