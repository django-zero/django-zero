import os
import shlex
import shutil
import subprocess
import sys

from mondrian import humanizer, term

import django_zero
from django_zero.commands import AbstractSubcommand
from django_zero.commands.utils.processes import call_manage, call_webpack, create_honcho_manager
from django_zero.utils import check_dev_extras, check_installed, check_prod_extras, get_env


class BaseLifecycleCommand(AbstractSubcommand):
    """
    Contains logic for all lifecycle-related commands.

    Abstract (does not implement `handle()`).

    """

    def execute(self, command, *, cwd, shell=True):
        self.logger.info(term.bold(">>> %s") + " " + term.lightblack("(in %s)"), command, cwd)

        retval = subprocess.call(command, cwd=cwd, shell=shell)

        if retval:
            self.logger.error(term.red(term.bold("... ✖ failed")))
            raise RuntimeError('"{}" returned {}.'.format(command, retval))
        else:
            self.logger.info(term.green(term.bold("... ✓ ok")))


class StartCommand(BaseLifecycleCommand):
    """Starts all processes using honcho, after calling eventual prerequisites."""

    def add_arguments(self, parser):
        parser.add_argument("--prod", "--production", "-p", action="store_true")
        parser.add_argument("--bind", default=None)
        parser.add_argument("--collectstatic", action="store_true")
        dev_server = parser.add_mutually_exclusive_group(required=False)
        dev_server.add_argument("--hot", action="store_true")
        dev_server.add_argument("--hot-only", action="store_true")

    def handle(self, *, bind=None, collectstatic=False, hot=False, hot_only=False, prod=False):
        from django_zero.config.settings import features

        cmd = "django-zero start"
        check_dev_extras(cmd)

        if prod:
            if hot or hot_only:
                raise RuntimeError(
                    "Cannot use webpack-dev-server (invluding --hot or --hot-only modes) in production mode."
                )
            if bind:
                raise NotImplementedError(
                    "Custom bind address/port can't be customized in production env (yet). Please open a pull-request!"
                )
            check_prod_extras(cmd)
            if features.is_webpack_enabled():
                call_webpack(environ={"NODE_ENV": "production"})
            if collectstatic:
                call_manage("collectstatic", "--noinput")
            m = create_honcho_manager(mode="prod")
        else:
            check_installed()
            m = create_honcho_manager(mode="dev", bind=bind, hot=hot, hot_only=hot_only, environ={"DJANGO_DEBUG": "1"})

        m.loop()
        return m.returncode


class InstallCommand(BaseLifecycleCommand):
    """Runs "yarn install" within the django-zero package, to make shared node dependencies available."""

    def add_arguments(self, parser):
        parser.add_argument("--dev", action="store_const", const="dev", dest="extra")
        parser.add_argument("--prod", action="store_const", const="prod", dest="extra")

    def handle(self, *more, extra=None):
        from django_zero.config.settings import features

        env = get_env()

        zero_dir = env["DJANGO_ZERO_BASE_DIR"]
        project_dir = env["DJANGO_BASE_DIR"]

        self.execute(
            sys.executable
            + " -m pip install --quiet {more} -e .{extra}".format(
                more=" ".join(map(shlex.quote, more)), extra="[" + extra + "]" if extra else ""
            ),
            cwd=project_dir,
        )
        if features.is_webpack_enabled():
            self.execute("yarn install --silent", cwd=zero_dir)
            self.execute("yarn install --silent", cwd=project_dir)

        print(
            humanizer.Success(
                "Project was installed successfully.",
                "Eventually run migrations, then spawn a dev server:",
                "",
                "  $ `django-zero manage migrate`",
                "  $ `django-zero start`",
            )
        )


class UninstallCommand(BaseLifecycleCommand):
    """Removes the "node_modules" directory within django-zero package."""

    def handle(self):
        check_installed()
        env = get_env()
        shutil.rmtree(os.path.join(env["DJANGO_ZERO_BASE_DIR"], "node_modules"))


class PathCommand(BaseLifecycleCommand):
    """Shows the path of django-zero package."""

    def handle(self):
        print(os.path.dirname(django_zero.__file__))
