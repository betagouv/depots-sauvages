#!/bin/bash
# This script is ran by scalingo to start the application

echo "🔄 Starting the Django app ($DJANGO_SETTINGS_MODULE)"

# Gunicorn worker recycling configuration to mitigate memory leaks
GUNICORN_MAX_REQUESTS=${GUNICORN_MAX_REQUESTS:-500}
GUNICORN_MAX_REQUESTS_JITTER=${GUNICORN_MAX_REQUESTS_JITTER:-50}

gunicorn backend.wsgi \
    --max-requests "$GUNICORN_MAX_REQUESTS" \
    --max-requests-jitter "$GUNICORN_MAX_REQUESTS_JITTER" \
    --log-file -
