#!/bin/bash
# This script is ran by scalingo to start the application

echo "🔄 Starting the post_deploy hook"

python manage.py migrate

echo "✅ Leaving the post_deploy hook"
