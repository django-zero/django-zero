import sys

if __name__ == "__main__":
    from django_zero.commands import main

    retval = main()
    sys.exit(int(retval) if retval else 0)
