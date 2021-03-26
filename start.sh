#!/bin/bash

PROJECT_NAME="ops"


# shellcheck disable=SC2126
if [[ $(ps -ef | grep -v grep | grep $PROJECT_NAME | wc -l) -lt 1 ]];then
  ./.venv/bin/gunicorn -c config/gunicorn.conf.py $PROJECT_NAME.wsgi:application
fi

sleep 1
ps -ef | grep -v "grep" | grep $PROJECT_NAME