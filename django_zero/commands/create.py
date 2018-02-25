import os

from django_zero.commands import BaseCommand


class CreateCommand(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--no-input', action='store_true')

        subparsers = parser.add_subparsers(dest='type')
        subparsers.required = True

        project = subparsers.add_parser('project')
        project.add_argument('path')

        app = subparsers.add_parser('app')
        app.add_argument('name')

    def handle(self, *args, **options):
        _type = options.pop('type')

        if _type == 'app':
            return self.handle_app(*args, **options)

        if _type == 'project':
            return self.handle_project(*args, **options)

    def handle_app(self, *args, **options):
        no_input = options.pop('no_input')
        name = options.pop('name')
        path = 'apps'

        template = os.path.join(os.path.dirname(__file__), 'templates/app')
        from cookiecutter.main import cookiecutter
        cookiecutter(template, checkout=False, output_dir=path, extra_context={'name': name, **options}, no_input=True)

        print('Your "{}" application has been created.'.format(name))
        print()
        print('Please add the following to your INSTALLED_APPS (in config/settings.py)')
        print()
        print("  INSTALLED_APPS += [")
        print("      ...,")
        print("      'apps.{}',".format(name))
        print("  ]")
        print()

    def handle_project(self, *args, **options):
        no_input = options.pop('no_input')
        path = options.pop('path')
        name = os.path.basename(path)
        path = os.path.dirname(path) or '.'

        template = os.path.join(os.path.dirname(__file__), 'templates/project')

        from cookiecutter.main import cookiecutter
        cookiecutter(template, checkout=False, output_dir=path, extra_context={'name': name, **options},
                     no_input=no_input)

        from medikit.commands import handle_update
        oldwd = os.getcwd()
        os.chdir(os.path.join(path, name))
        try:
            handle_update('Projectfile')
        finally:
            os.chdir(oldwd)
