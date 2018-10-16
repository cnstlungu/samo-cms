#!/bin/bash
source venv/bin/activate
celery worker -A samo.core.celery --loglevel=info
