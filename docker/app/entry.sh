#!/bin/bash
source venv/bin/activate
python manage.py migrations upgrade
python manage.py create_admin
exec gunicorn -w 8 -b :5000 --access-logfile - --error-logfile - samo:app
