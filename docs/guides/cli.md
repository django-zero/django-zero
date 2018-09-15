# Command Line

The `django-zero` command line tool will help you manage your project. It is *not* the `django-admin` or `manage.py`
script that is available in usual `django` projects, although you can run the django management tool from the CLI.

## General considerations

You can run the CLI either from the console script, or by executing the module. The two following commands are
equivalent:

```bash
$ django-zero
``` 

```bash
$ python -m django_zero
``` 

The CLI consists of "subcommands", available from the entrypoint command described above. You can obtain more
informations by setting python's logging level to DEBUG, using the `--debug` flag (or `-D`).

```bash
$ django-zero [--debug|-D] <subcommand>
``` 

or using the module...

```bash
$ python -m django_zero [--debug|-D] <subcommand>
``` 

## Scaffolding commands

`django-zero` contains some `cookiecutter` templates to help you scaffold your projects.

### Project creation

To create a new `django-zero` project:

```bash
$ django-zero create project <project-name>
```

Command will create a new directory with the provided name, ready to roll.

### App creation

Once you're in a project, you can use the app creation script:

```bash
$ django-zero create app <app-name>
```

By convention, the application will live in `apps/<app-name>`.

## Lifecycle commands

Lifecycle commands will help you during development and deployment.

### Install

Updates project dependencies, both local (to your project) and global (to one `django-zero` install, in a virtualenv
for example). Python package install is not enough, as this will also install Node.js modules.

```bash
$ django-zero install
```

### Uninstall

Cleanup Node.js modules.

```bash
$ django-zero uninstall
```

### Start

Starts a `honcho` manager with the necessary subprocesses to have de development server. This will launch django's
development server, but also webpack in "watch" mode (so your ES6/SCSS assets are recompiled when they change) and
maybe some more processes (for example, if you enable celery, it will run both celery beat and a celery worker).

```bash
$ django-zero start
```

### Path

Output `django-zero`'s library path.

```bash
$ django-zero path
```

## Delegation commands

Most things done by the CLI requires to delegate work to subprocesses, after a bit of environment setup. Instead of
running `webpack`, `gunicorn`, `django-admin`, `daphne`, `celery`, etc. you should prefer the delegate subcommands so
you're certain the environment is correct.

::: tip
One of the trickiest parts is that instead of just relying on the project's `node_modules` directory, we setup the
environment so that Node.js will use both your project's `node_modules` directory but also `django-zero`'s
`node_modules`.

It allows to bundle javascript dependencies with the library, while giving you the freedom of depending on whatever you
want and not requiring to bundle the actual javascript files into `django-zero`'s releases.
:::

::: tip
All delegates commands allow to pass arbitrary parameters to the actual binary handler. For example, if you want to
pass the `--wonderfull` flag to `webpack`, just run `django-zero webpack --wonderfull`.
:::


### Manage (django-admin)

```bash
$ django-zero manage ...
```

### Gunicorn

```bash
$ django-zero gunicorn ...
```

(requires `gunicorn` to be installed)

### Daphne

```bash
$ django-zero daphne ...
```

(requires `channels` and `daphne` to be installed)

### Celery

```bash
$ django-zero celery ...
```

(requires `celery` to be installed and enabled)

### Webpack

```bash
$ django-zero webpack ...
```
