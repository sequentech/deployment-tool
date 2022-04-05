#!/bin/bash

# This file is part of deployment-tool.
# Copyright (C) 2014-2016  Sequent Tech Inc <legal@sequentech.io>

# deployment-tool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# deployment-tool  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with deployment-tool.  If not, see <http://www.gnu.org/licenses/>.

PIDFILE=/var/run/syncdirs.pidfile

trap "{ [ -f $PIDFILE ] && kill -9 $(cat $PIDFILE) }" SIGINT SIGTERM

while true
do
  rsync -avz -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" ballotbox@{{ config.load_balancing.slave.master_hostname }}:/home/ballotbox/datastore/ /home/ballotbox/datastore/
  rsync -avz -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" ballotbox@{{ config.load_balancing.slave.master_hostname }}:/srv/certs/selfsigned/ /srv/certs/selfsigned/
  sleep {{ config.load_balancing.slave.rsync_update_secs }}

done