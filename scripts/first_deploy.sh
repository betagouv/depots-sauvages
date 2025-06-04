#!/bin/bash

# This script is used by scalingo and is meant to run on Review Apps.
# When operating the first deployment of the application, it replaces
# the post deploy hook.

echo "🔄 Running first deploy script for review app..."
PG_OPTIONS="--clean --if-exists --no-owner --no-privileges --no-comments"
PG_EXCLUDE_SCHEMA="-N 'information_schema' -N '^pg_*'"
dbclient-fetcher psql # Fetch the new version of the PostgreSQL client
/app/bin/pg_dump $PG_OPTIONS $PG_EXCLUDE_SCHEMA --dbname $PARENT_POSTGRESQL_URL --format c --file /tmp/dump.pgsql
sleep 5 # Pause while SGBD loading
/app/bin/pg_restore $PG_OPTIONS --dbname $SCALINGO_POSTGRESQL_URL /tmp/dump.pgsql

python scripts/check_existing_users.py

# We want to include commands from the post deploy hook as well:
bash $HOME/scripts/post_deploy.sh
echo "✅ First deploy script completed"