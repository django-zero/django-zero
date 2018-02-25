from django_zero.commands import BaseCommand
from django_zero.processes import create_honcho_manager, call_webpack, call_manage
from django_zero.utils import check_installed


class StartCommand(BaseCommand):
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
