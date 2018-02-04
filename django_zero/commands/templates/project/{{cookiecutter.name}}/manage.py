import sys

if __name__ == '__main__':
    from django_zero.__main__ import handle_manage
    handle_manage(*sys.argv[1:])
