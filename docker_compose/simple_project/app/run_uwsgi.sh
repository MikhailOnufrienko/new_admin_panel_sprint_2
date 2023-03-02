#!/usr/bin/env bash

set -e

chown djus:djus /var/log

uwsgi --strict --ini /etc/app/uwsgi.ini
