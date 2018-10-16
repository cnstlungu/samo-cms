#!/usr/bin/env bash
cd /home/dev/repos/samo-cms/
export FLASK_ENV="development"
source venv/bin/activate
celery worker -A samo.core.celery --loglevel=info