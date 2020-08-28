#!/usr/bin/env bash

python manage.py makemigrations
python manage.py migrate
python manage.py seed_db
python manage.py guild_seed_db
python manage.py collectstatic --noinput

#python manage.py runserver 0.0.0.0:5005

gunicorn -cpython:gunicorn_config -b ${DJANGO_BIND_ADDRESS}:${DJANGO_BIND_PORT} chat_wars_database.wsgi
