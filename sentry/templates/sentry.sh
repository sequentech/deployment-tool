#!/bin/bash

# https://stackoverflow.com/questions/9090683/supervisord-stopping-child-processes
# This kills the entire process group when the main script exits, such as when it is killed by supervisord.
# One of the processes that is usually left hanging is vfork.
# Note that this is suposedly already handled by supervisor, but we do it also
# here just in case.
trap "kill -9 -- -$$" EXIT

/home/sentry/venv/bin/sentry --config=/home/sentry/sentry.conf.py start