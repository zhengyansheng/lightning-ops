#!/bin/bash

PROJECT_NAME="ops"

# process ansible api return empty
export PYTHONOPTIMIZE=1

# start celery
celery -A $PROJECT_NAME.celery worker -l debug

sleep 1