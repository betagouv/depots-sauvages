#!/bin/bash
# This script is ran by scalingo to start the application

echo "Starting the Django app ($DJANGO_SETTINGS_MODULE)"

gunicorn backend.wsgi --log-file -
