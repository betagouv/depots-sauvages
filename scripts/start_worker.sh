#!/bin/bash
# This script starts the django-tasks worker for the all queues

echo "Starting django-tasks worker..."

python manage.py db_worker