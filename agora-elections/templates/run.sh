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

/home/agoraelections/agora-elections/target/universal/stage/bin/agora-elections -v -Dconfig.file=/home/agoraelections/agora-elections/conf/application.conf