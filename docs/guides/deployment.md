# Deployment

We're working on this part.

Here is a minimal docker recipe that you can use:

```dockerfile
FROM okdocker/pynode:3.6-8.x

# Work directory
RUN mkdir /usr/local/project
WORKDIR /usr/local/project

COPY . ./
RUN pip install -r requirements-prod.txt gunicorn==19.9.0
RUN django-zero install
RUN django-zero webpack -p
RUN django-zero manage collectstatic --noinput
RUN django-zero manage migrate
CMD django-zero gunicorn --bind 0.0.0.0
```

Stay tuned for more options, or better written recipes.