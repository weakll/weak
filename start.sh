#!/bin/bash
set -e

echo "=== Running migrations ==="
python manage.py migrate --noinput

echo "=== Seeding initial data ==="
python manage.py seed_all --noinput || echo "Seed skipped (data may already exist)"

echo "=== Starting gunicorn on 0.0.0.0:$PORT ==="
gunicorn night_market.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120
