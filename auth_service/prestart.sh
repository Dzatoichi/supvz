#!/usr/bin/env bash

set -e

echo "Run apply migrations..."
alembic upgrade head
echo "Migrations applied!"

echo "Initial database data..."
python -m src.initial_data
echo "Data successfully added"

exec "$@"