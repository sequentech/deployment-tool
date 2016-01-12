#!/bin/bash

function finish {
  echo finishing
  ps auxww | grep '^sentry ' | grep 'celery' | awk '{print $2}' | xargs kill -9
}
trap finish EXIT SIGINT

/home/sentry/venv/bin/sentry --config=/home/sentry/sentry.conf.py celery worker -B