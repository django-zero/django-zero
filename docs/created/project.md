# Your project was created

Contratulations, you created a brand new **django-zero** project. 
It's basically a standard **django** project with superpowers.

## Getting started

```bash
$ cd /path/to/your/project
```

Before the project is ready, you need to install some dependencies, including JavaScript dependencies.

```bash
$ django-zero install
```
    
It will use `yarn` to install javascript dependencies both in `django-zero` package and in your project.

Install python dependencies and run django migrations:

```bash
$ make install-dev
$ django-zero manage migrate
```

To start the django development server, run:

```bash
$ django-zero start
```
    
Or alternativelly:

```bash
$ make
```
    
## Directory structure

As a default, django-zero projects contains the following directory structure:

### Apps

This is an empty directory ready to welcome your project-specific django applications. You can create a new application
running:

```bash
$ django-zero create app hello
```

### Config

This contains all configuration-related files. Most importantly, you'll find here:

* `settings.py`: your django settings
* `urls.py`: your root urls configuration
* `jinja2.py`: your jinja2 environment
* `wsgi.py`: your wsgi application
* `webpack.js`: your webpack build configuration

All those files import their defaults from **django-zero**. You can override whatever you feel to, but you won't
repeat yourself when it comes to reasonable defaults.

### Resources

This contains all the non-python code and assets that are global to your project.

* `assets`: your source scripts (ES6 out of the box) and styles (SASS out of the box) 
* `jinja2`: your jinja2 templates
* `static`: your static files
* `templates`: your DTL templates

Each app will have an optional `resources` directory that can contains the same subdirectories, so don't feel like
you have to make it global. It's just there so things that does not really belongs to an app can find a place to live.

## What next?

A project is great, but your django code should usually mostly live in applications.

- [Create a django (zero) application](../howto/create-an-application.md)

Already a pro?

- [Jump in the Guide](../guides/)
