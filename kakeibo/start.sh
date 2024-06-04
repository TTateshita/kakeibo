#!/bin/bash

./manage.py migrate --noinput
./manage.py collectstatic --noinput
./manage.py createcachetable

gunicorn kakeibo.wsgi --bind 0.0.0.0:8000