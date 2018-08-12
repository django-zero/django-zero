# Installation

You need `python 3.5+` installed, with `pip`.

You also need `Node.js` (LTS or Current), with `yarn`.

Please note that `django-zero` will need permissions to write files in its own package, you really should install it in userland, for example in a nice and shiny virtual environment (yes, it is important).

```bash
$ pip install django-zero[dev]
``` 

That's it, you can jump to the [getting started →](./getting-started.md) guide.

::: tip
Django-zero write in its own package, because it contains javascript dependencies in `package.json` and `yarn.lock`
files, and the associated package manager (`yarn`) will need to expand the packages into a `node_modules` directory
there.

This is necessary so that the javascript dependencies are treated like a python dependency, while keeping the release
process simple. We publish the `package.json`/`yarn.lock` files within the python egg on PyPI, you get the freezed
javascript dependencies (but you still download them from NPM, the Node.js package repository).
:::
