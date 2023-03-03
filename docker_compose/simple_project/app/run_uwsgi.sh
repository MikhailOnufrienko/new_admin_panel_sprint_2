#!/usr/bin/env bash

set -e

chown djus:djus /var/log

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py collectstatic --noinput
python manage.py migrate
uwsgi --strict --ini /app/uwsgi.ini

exec "$@"

