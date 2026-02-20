#!/bin/bash
set -e

echo "🔄 Ensuring documents directory exists..."
mkdir -p /app/documents
chmod 777 /app/documents

echo "🔄 Running migrations..."
python manage.py migrate --noinput

if [ "$DJANGO_COLLECT_STATIC" = "true" ]; then
    echo "🔄 Collecting static files..."
    python manage.py collectstatic --noinput
fi

if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "🔄 Creating superuser - ignore errors if already exists..."
    python manage.py createsuperuser --noinput || true  # Ignore errors on superuser creation
fi

case "$1" in
    runserver)
        echo "🚀 Starting development server..."
        exec python manage.py runserver 0.0.0.0:8000
        ;;
    gunicorn)
        echo "🚀 Starting production server..."
        exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000
        ;;
    *)
        echo "🚀 Executing command: $@"
        exec "$@"
        ;;
esac 