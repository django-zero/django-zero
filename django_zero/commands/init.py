import os

from django_zero.commands import BaseCommand


class InitCommand(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--no-input', action='store_true')

        subparsers = parser.add_subparsers(dest='type')
        subparsers.required = True

        project = subparsers.add_parser('project')
        project.add_argument('path')

    def handle(self, *args, **options):
        _type = options.pop('type')

        if _type == 'project':
            return self.handle_project(*args, **options)

    def handle_project(self, *args, **options):
        no_input = options.pop('no_input')
        path = options.pop('path')
        name = os.path.basename(path)
        path = os.path.dirname(path) or '.'

        template = os.path.join(os.path.dirname(__file__), 'templates/project')

        from cookiecutter.main import cookiecutter
        cookiecutter(template, checkout=False, output_dir=path, extra_context={'name': name, **options},
                     no_input=no_input)
