import os

import django_zero
import mondrian
from django_zero.commands.base import BaseCommand
from django_zero.utils import check_dev_extras, url_for_help


class CreateCommand(BaseCommand):
    """Create a project/an app."""

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="type")
        subparsers.required = True

        project = subparsers.add_parser("project")
        project.add_argument("path")

        app = subparsers.add_parser("app")
        app.add_argument("name")

    def handle(self, *args, **options):
        _type = options.pop("type")

        with mondrian.humanizer.humanize():
            if _type == "app":
                return self.handle_app(*args, **options)

            if _type == "project":
                return self.handle_project(*args, **options)

    def handle_app(self, *args, **options):
        check_dev_extras("django-zero create app")

        name = options.pop("name")
        path = "apps"

        template = os.path.join(os.path.dirname(__file__), "templates/app")
        from cookiecutter.main import cookiecutter

        cookiecutter(template, checkout=False, output_dir=path, extra_context={"name": name, **options}, no_input=True)

        print(
            mondrian.humanizer.Success(
                'Your "{}" application has been created.'.format(name),
                "Add the following to your `INSTALLED_APPS` in `config/settings.py`:",
                "",
                "INSTALLED_APPS += [",
                "    ...,",
                "    `'apps.{}',`".format(name),
                "]",
                help_url=url_for_help("created/app.html"),
            )
        )

    def handle_project(self, *args, **options):
        check_dev_extras("django-zero create project")

        path = options.pop("path")
        name = os.path.basename(path)
        path = os.path.dirname(path) or "."

        template = os.path.join(os.path.dirname(__file__), "templates/project")

        from cookiecutter.main import cookiecutter

        cookiecutter(template, checkout=False, output_dir=path, extra_context={"name": name, **options}, no_input=True)

        from medikit.commands import handle_update

        oldwd = os.getcwd()
        os.chdir(os.path.join(path, name))
        try:
            handle_update("Projectfile")
        finally:
            os.chdir(oldwd)

        print(
            mondrian.humanizer.Success(
                'Project "{}" has been created.'.format(name),
                "Install your project and launch django's development server:",
                "",
                "  $ `cd {}`".format(name),
                "  $ `django-zero install`",
                "  $ `make`",
                "",
                "Development server will listen on `http://127.0.0.1:8000/`",
                help_url=url_for_help("created/project.html"),
            )
        )
