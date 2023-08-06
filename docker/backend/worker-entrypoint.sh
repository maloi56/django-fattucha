#!/bin/sh

until cd /app/backend/fattucha
do
    echo "Waiting for server volume..."
done

# run a worker :)
celery -A fattucha worker --loglevel=info --concurrency 1 -E