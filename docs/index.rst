Django Zero
===========

Django Zero helps creating and maintaining fully-featured modern django applications.

Instead of having boilerplate settings, we set reasonable defaults and let you override only the non-standard parts.

Out of the box, you'll get a working and ready-to-deploy project with javascript and sass styles compiled using webpack,
jinja2 templating language, authentication (including social authentication) using allauth, whitenoise to serve assets
and a bunch more features.

Quick start
:::::::::::

You need Node.js 8+ with Yarn and a working python 3.5+ environment where your user have write permissions (for example,
a virtualenv).

.. code-block:: shell-session

   $ pip install django-zero[dev]
   $ django-zero create-project acme
   $ cd acme
   $ make

Your website should now be available on http://localhost:8000/, enjoy!

Table of Content
::::::::::::::::

.. toctree::
   :maxdepth: 2

   features

Indexes
:::::::

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
