import os
from collections import namedtuple

from django.conf import settings
from django.http import Http404
from django.shortcuts import render

Feature = namedtuple("Feature", ["name", "category", "description"])

FEATURES = {
    "webpack": Feature(
        name="Webpack",
        category="Assets Management",
        description="Assets are compiled using webpack. Default configuration provides Babel and Sass, tuneable at will.",
    ),
    "jinja2": Feature(
        name="Jinja 2",
        category="Templating",
        description="Jinja2 templating engine is installed and configured, with django-friendly filters and globals.",
    ),
    "bootstrap": Feature(
        name="Bootstrap 4",
        category="Frontend",
        description="The modern frontend framework.\nEither use the default version or customize its build.",
    ),
    "allauth": Feature(
        name="Allauth",
        category="Authentication",
        description="User management is pre-configured, with matching views. Adding OAuth providers is a matter of pasting your keys.",
    ),
    "docker": Feature(
        name="Docker & Rocker",
        category="Packaging",
        description="Build production ready images using either Docker or Rocker.",
    ),
    "debug": Feature(
        name="Toolbar & Extensions",
        category="Debugging",
        description="Development server enables both django-extensions and django-debug-toolbar.",
    ),
    "cookiecutter": Feature(
        name="Cookiecutter",
        category="Scaffolding",
        description="Create projects and applications in seconds, using the interactive cookiecutter templates.",
    ),
    "mondrian": Feature(
        name="Mondrian",
        category="Logging",
        description="Configure and extend the python logging facilities without even thinking about it.",
    ),
    "gunicorn": Feature(
        name="Gunicorn",
        category="Production Server",
        description="Battle-tested production server at your fingertips, packaged for take-away.",
    ),
    "whitenoise": Feature(
        name="Whitenoise",
        category="Assets Server",
        description="Like static files, but better (including compression and brotli support)!",
    ),
    "honcho": Feature(
        name="Honcho",
        category="Process Manager",
        description="Manage all the necessary processes running in parallel and keep your console readable.",
    ),
    "pytest": Feature(
        name="Pytest",
        category="Testing",
        description="Write tests for your code and make sure you are dead serious about output quality!",
    ),
}


def example_feature_list_view(request):
    return render(request, "examples/feature_list.html", {"features": FEATURES})


def example_feature_detail_view(request, slug):
    try:
        feature = FEATURES[slug]
    except KeyError:
        raise Http404("Feature not found.")

    parsed = None
    filename = os.path.join(settings.ZERO_DIR, "../docs/features", slug + ".rst")

    if os.path.exists(filename):
        try:
            from docutils.core import publish_parts

            with open(filename) as f:
                parsed = publish_parts(f.read(), writer_name="html5")
        except ImportError:
            parsed = {
                "body": "Please install python's <code>docutils</code> package to render the detail pages of demo application."
            }

    return render(
        request, "examples/feature_detail.html", {"current_feature": feature, "features": FEATURES, "content": parsed}
    )
