#!/bin/sh

set -e
set -x

python manage.py migrate

python manage.py collectstatic --noinput

gunicorn -t 300 --keep-alive 5 --threads 3 -b 0.0.0.0:8000 ecommerce.wsgi
