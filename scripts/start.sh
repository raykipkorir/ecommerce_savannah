#!/bin/sh

set -e
set -x

python manage.py migrate

python manage.py collectstatic --noinput

gunicorn ecommerce.wsgi -t 1200 --keep-alive 1200 -b 0.0.0.0:8000
