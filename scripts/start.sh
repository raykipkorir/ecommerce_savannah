#!/bin/sh

set -e
set -x

python manage.py migrate

python manage.py collectstatic --noinput

gunicorn ecommerce.wsgi -b 0.0.0.0:8000
