#!/bin/bash
set -e

echo "=== Running migrations ==="
python manage.py migrate --noinput

echo "=== Seeding initial data ==="
python manage.py seed_all --noinput || echo "Seed skipped"

echo "=== Creating default superuser ==="
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', '', 'admin123')
    print('Superuser created: admin / admin123')
else:
    print('Superuser already exists')
" 2>&1 || echo "Superuser check done"

echo "=== Starting gunicorn on 0.0.0.0:$PORT ==="
gunicorn night_market.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120
