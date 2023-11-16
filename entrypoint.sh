#!/bin/bash

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate --noinput

python manage.py wait_for_db

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn avikus.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
