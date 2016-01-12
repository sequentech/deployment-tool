#!/bin/bash

PID_FILE=/home/agoraelections/agora-elections/target/universal/stage/RUNNING_PID
if [ -f "$PID_FILE" ]
then
    kill -9 $(cat "$PID_FILE")
    rm "$PID_FILE"
fi

# fixes errors on non-ascii characters
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

# https://stackoverflow.com/questions/9090683/supervisord-stopping-child-processes
# This kills the entire process group when the main script exits, such as when it is killed by supervisord.
# One of the processes that is usually left hanging is vfork.
# Note that this is suposedly already handled by supervisor, but we do it also
# here just in case.
trap "kill -9 -- -$$" EXIT

/home/agoraelections/agora-elections/target/universal/stage/bin/agora-elections -v -Dconfig.file=/home/agoraelections/agora-elections/conf/application.conf