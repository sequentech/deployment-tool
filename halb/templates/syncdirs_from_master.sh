#!/bin/bash

PIDFILE=/var/run/syncdirs.pidfile

trap "{ [ -f $PIDFILE ] && kill -9 $(cat $PIDFILE) }" SIGINT SIGTERM

while true
do
  rsync -avz -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" agoraelections@{{ config.load_balancing.slave.master_hostname }}:/home/agoraelections/datastore/ /home/agoraelections/datastore/
  rsync -avz -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" agoraelections@{{ config.load_balancing.slave.master_hostname }}:/srv/certs/selfsigned/ /srv/certs/selfsigned/
  sleep {{ config.load_balancing.slave.rsync_update_secs }}

done