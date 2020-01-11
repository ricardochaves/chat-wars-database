#!/usr/bin/env bash

python manage.py migrate
python manage.py collectstatic --noinput


if [[ ${DJANGO_BIND_ADDRESS+x} ]] && [[ ${DJANGO_BIND_PORT+x} ]];
then
    echo "OK! Using custom ADRESSS $DJANGO_BIND_ADDRESS and PORT $DJANGO_BIND_PORT"
    gunicorn -cpython:gunicorn_config -b ${DJANGO_BIND_ADDRESS}:${DJANGO_BIND_PORT} chat_wars_database.wsgi
else
    echo "Using 0.0.0.0:8000"
    gunicorn -cpython:gunicorn_config -b 0.0.0.0:8080 chat_wars_database.wsgi
fi