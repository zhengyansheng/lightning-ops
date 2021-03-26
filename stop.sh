#!/bin/bash

PROJECT_NAME="ops"

ps -ef |grep -v 'grep' | grep $PROJECT_NAME | awk '{ print $2 }' | xargs kill