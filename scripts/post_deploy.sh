#!/bin/bash
# This script is ran by scalingo to start the application

echo "🔄 Starting the post_deploy hook"

python manage.py migrate

if [ "$STATS_ENABLED" = "true" ] || [ -n "$STATS_DATABASE_URL" ]; then
    echo "🔄 Migrating stats database..."
    python manage.py migrate --database=stats_db
fi

echo "✅ Leaving the post_deploy hook"
