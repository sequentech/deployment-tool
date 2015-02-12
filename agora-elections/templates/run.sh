#!/bin/bash

# fixes errors on non-ascii characters
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

/home/agoraelections/agora-elections/target/universal/stage/bin/agora-elections -v -Dconfig.file=/home/agoraelections/agora-elections/conf/application.conf