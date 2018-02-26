import sys

from django_zero.commands import main

if __name__ == '__main__':
    retval = main()

    if retval:
        sys.exit(int(retval))
