#!/bin/bash

function finish {
  echo finishing
  ps auxww | grep '^authapi ' | grep 'celery' | awk '{print $2}' | xargs kill -9
}
trap finish EXIT SIGINT

/home/authapi/env/bin/python manage.py celeryd -B --settings=authapi.deploy
