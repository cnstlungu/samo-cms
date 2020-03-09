#!/usr/bin/env bash
cd ..
FLASK_ENV=${FLASK_ENV:-"development"}
export FLASK_ENV
source venv/bin/activate
python -m pylint samo