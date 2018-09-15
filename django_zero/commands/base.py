import logging


class AbstractSubcommand:
    """
    Base class for django-zero's subcommands.

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
        raise NotImplementedError("Subclasses of BaseCommand must provide a handle() method")

    @classmethod
    def is_enabled(cls):
        return True
