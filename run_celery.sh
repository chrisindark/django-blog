#! /bin/sh

# wait for rabbitmq server to start
#sleep 10

# run celery worker with any config stored
python manage.py celery worker -B --loglevel=INFO
