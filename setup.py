# Generated by Medikit 0.8.0 on 2022-01-10.
# All changes will be overriden.
# Edit Projectfile and run “make update” (or “medikit update”) to regenerate.

from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Py3 compatibility hacks, borrowed from IPython.
try:
    execfile
except NameError:

    def execfile(fname, globs, locs=None):
        locs = locs or globs
        exec(compile(open(fname).read(), fname, "exec"), globs, locs)


# Get the long description from the README file
try:
    with open(path.join(here, "README.rst"), encoding="utf-8") as f:
        long_description = f.read()
except:
    long_description = ""

# Get the classifiers from the classifiers file
tolines = lambda c: list(filter(None, map(lambda s: s.strip(), c.split("\n"))))
try:
    with open(path.join(here, "classifiers.txt"), encoding="utf-8") as f:
        classifiers = tolines(f.read())
except:
    classifiers = []

version_ns = {}
try:
    execfile(path.join(here, "django_zero/_version.py"), version_ns)
except EnvironmentError:
    version = "dev"
else:
    version = version_ns.get("__version__", "dev")

setup(
    author="Romain Dorgueil",
    author_email="romain@dorgueil.net",
    description="Zero-configuration django projects.",
    license="Apache License, Version 2.0",
    name="django_zero",
    version=version,
    long_description=long_description,
    classifiers=classifiers,
    packages=find_packages(exclude=["ez_setup", "example", "test"]),
    include_package_data=True,
    install_requires=[
        "brotli ~= 1.0.9",
        "django ~= 3.2, < 3.3",
        "django-allauth ~= 0.47.0",
        "jinja2 ~= 3.0.3",
        "mondrian ~= 0.8",
        "whitenoise ~= 5.3.0",
    ],
    extras_require={
        "celery": [
            "celery ~= 5.0",
            "django ~= 3.2, < 3.3",
            "django_celery_beat ~= 2.2.1",
            "django_celery_results ~= 2.2.0",
        ],
        "channels": ["channels ~= 3.0.0", "daphne ~= 3.0.0", "django ~= 3.2, < 3.3"],
        "dev": [
            "cookiecutter ~= 1.7",
            "coverage ~= 6.2",
            "django ~= 3.2, < 3.3",
            "django-extensions ~= 3.1",
            "django_debug_toolbar ~= 3.2",
            "honcho ~= 1.0",
            "isort",
            "medikit ~= 0.7",
            "pyquery ~= 1.4",
            "pytest >= 5.4.0",
            "pytest-cov ~= 3.0.0",
            "pytest-django ~= 4.0",
            "werkzeug ~= 2.0",
        ],
        "prod": ["django ~= 3.2, < 3.3", "gunicorn ~= 20.0"],
    },
    entry_points={"console_scripts": ["django-zero = django_zero.commands:main"]},
    url="https://github.com/hartym/django-zero",
    download_url="https://github.com/hartym/django-zero/archive/{version}.tar.gz".format(version=version),
)
