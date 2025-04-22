#!/bin/sh
set -e

echo "🔄 Ensuring dependencies are up to date..."
yarn install

if [ "$1" = "dev" ]; then
    echo "🚀 Starting development server..."
    exec yarn dev --host=0.0.0.0
elif [ "$1" = "build" ]; then
    echo "📦 Building production bundle..."
    exec yarn build
elif [ "$1" = "preview" ]; then
    echo "👁️ Starting preview server..."
    exec yarn preview --host=0.0.0.0
else
    echo "🚀 Executing command: $@"
    exec "$@"
fi 