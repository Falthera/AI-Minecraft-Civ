#!/bin/bash
# Pterodactyl startup script for AI Controller
set -e

# Wait for PostgreSQL
echo "Waiting for PostgreSQL..."
while ! pg_isready -h postgres -p 5432 -U ai_civilization >/dev/null 2>&1; do
    sleep 2
done
echo "PostgreSQL is ready."

# Run migrations (if any)
# python -m controller.db.migrate

# Start controller
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
