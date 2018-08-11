import sys

if __name__ == "__main__":
    from django_zero.commands.delegates import DjangoCommand

    django_command = DjangoCommand()
    django_command.handle(*sys.argv[1:])
