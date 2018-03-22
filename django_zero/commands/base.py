import logging

from django_zero.errors import UserError


class BaseCommand:
    """
    Base class for CLI commands.

    """

    @property
    def logger(self):
        try:
            return self._logger
        except AttributeError:
            self._logger = logging.getLogger(type(self).__name__)
            return self._logger

    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        """
        pass

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement this method.
        """
        raise NotImplementedError('Subclasses of BaseCommand must provide a handle() method')
