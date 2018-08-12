# Development





Debug
=====

For development environments, `django-zero` is bundled with `django-debug-toolbar` and `django-extensions`.

This is not something you'd want in a production environment, so you must install the dependencies using the `dev`
extra.

Even if installed, the dependencies are only activated if `DEBUG==True`.

.. code-block:: shell-session

    $ pip install django-zero[dev]
    $ django-zero start

Django Debug Toolbar
::::::::::::::::::::

**Django Debug Toolbar** is a django applications that adds debug information to the HTML output of Django. You'll see it
on the right of your browser.

* `Read django-debug-toolbar's documentation <https://django-debug-toolbar.readthedocs.io/>`_

Django Extensions
:::::::::::::::::

**Django Extensions** adds a bunch of features to the django framework, but mostly, a bunch of commands to help you
develop faster, and an integration of an alternate development server based on Werkzeug that enables the "Don't Panic"
debugger, a better exception output that allows to interract with exception frames directly from your browser.

* `Read django-extensions' documentation <https://django-extensions.readthedocs.io/>`_
* `Read werkzeug's debugger documentation <http://werkzeug.pocoo.org/docs/0.14/debug/>`_


