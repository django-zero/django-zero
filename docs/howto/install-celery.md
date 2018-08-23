# How to install Celery

## Install the extra

To install celery related dependencies, django-zero provides an extra dependency.

```shell
$ pip install django-zero[celery]
```

You can combine extra dependencies, for example

```shell
$ pip install django-zero[celery,dev]
```

Of course, you can also setup the celery dependencies yourself, if you prefer to
have more fine-grained control over the requirements.

## Create the celery configuration

```python
import os

from celery import Celery

import django_zero

django_zero.configure(os.path.dirname(os.path.dirname(__file__)))

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
```

## Tune django settings

You can tune celery settings in `config/settings.py`, uppercasing and prefixing the celery settings
with `CELERY_`.

```python
...

# Celery
CELERY_BEAT_SCHEDULE = {}
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_RESULT_BACKEND = "django-db"
CELERY_TIMEZONE = TIME_ZONE
```

## Enable the feature

Open `config/__init__.py` and add:

```python
import os

# Celery
os.environ["ENABLE_CELERY"] = os.environ.get('ENABLE_CELERY', 'true')
from config.celery import app
```

* Ensure celery app is loaded.
* Adds celery processes to django-zero managed processes.

## Running in development

Now, by default, running the django-zero development server will spawn two more processes.

* Celery worker: to actually do things
* Celery beat: to schedule things

If you don't want those processes to run, you can always disable the feature temporarily:

```shell
$ ENABLE_CELERY=false django-zero start
```

Or using make...

```shell
$ ENABLE_CELERY=false make
```

