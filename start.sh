#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn restPlatform.wsgi:application \
    --bind 127.0.0.1:8000 \
    --workers 3