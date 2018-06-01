import os

BASE_DIR = os.environ.get('DJANGO_BASE_DIR', os.getcwd())
ZERO_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
