#!/usr/bin/env bash

set -e

chown djus:djus /var/log

python manage.py collectstatic --noinput
python manage.py migrate
uwsgi --strict --ini /app/uwsgi.ini
