#!/bin/sh
set -e

# Optionally wait for dependent services (e.g., postgres) here if needed

# Apply migrations
python manage.py migrate

# Start Gunicorn
exec gunicorn base_app.wsgi:application \
  --workers 3 \
  --bind 0.0.0.0:8000 \
  --log-level info
