# How to install Celery

First, open `config/__init__.py` and add:

```python
import os

os.environ['ENABLE_CELERY'] = 'true'
```