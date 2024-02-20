#!/bin/sh

set -e
set -x

python manage.py migrate

python manage.py collectstatic --noinput

gunicorn ecommerce.wsgi -t 120 -keep-alive 120 -b 0.0.0.0:8000
