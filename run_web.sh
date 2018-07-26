#! /bin/sh

# wait for postgresql server to start
#sleep 10

# migrate db
python manage.py migrate

# start development server on public ip
python manage.py runserver 0.0.0.0:8000
