#!/bin/bash
# ./results.sh -t tally.tar.gz -c config.json -s

# fixes errors on non-ascii characters
declare -x LANG="en_GB.UTF-8"
declare -x LANGUAGE="en_GB:en"

AGORA_RESULTS=/home/agoraelections/agora-results
VENV=/home/agoraelections/renv
source $VENV/bin/activate
$AGORA_RESULTS/agora-results $*
