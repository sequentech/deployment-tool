#!/bin/bash

# This file is part of agora-dev-box.
# Copyright (C) 2014-2016  Agora Voting SL <agora@agoravoting.com>

# agora-dev-box is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# agora-dev-box  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with agora-dev-box.  If not, see <http://www.gnu.org/licenses/>.


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

/home/agoraelections/agora-elections/target/universal/stage/bin/agora-elections \
    -v \
    -Dconfig.file=/home/agoraelections/agora-elections/conf/application.conf \
    -Dlogger.file=/home/agoraelections/agora-elections/conf/logback.xml
