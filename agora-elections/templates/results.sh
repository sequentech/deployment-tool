#!/bin/bash
# ./results.sh -t tally.tar.gz -c config.json -s
AGORA_RESULTS=/home/agoraelections/agora-results
VENV=/home/agoraelections/renv
source $VENV/bin/activate
$AGORA_RESULTS/agora-results $*
