#!/bin/bash

/home/leaf3/venv/bin/python manage.py migrate
/home/leaf3/venv/bin/python manage.py collectstatic --noinput
/home/leaf3/venv/bin/gunicorn --user leaf3 --bind 0.0.0.0:8181 conf.wsgi:application
