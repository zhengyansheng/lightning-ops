#!/bin/bash
source .venv/bin/activate
kill -9 `ps -ef | grep 9999 | grep -v grep | awk '{print $2}'`
nohup python manage.py runserver 0.0.0.0:9999 &
