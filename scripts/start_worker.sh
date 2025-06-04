#!/bin/bash

echo "🔄 Starting django-tasks worker for app ($DJANGO_SETTINGS_MODULE)..."

python manage.py db_worker --queue default --queue documents
