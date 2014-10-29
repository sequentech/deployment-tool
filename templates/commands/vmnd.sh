#!/bin/bash
EORCHESTRA=/home/eorchestra/
source $EORCHESTRA/.verificatum_env
COMMAND="vmnd -i json /home/eorchestra/election-orchestra/datastore/private/$1/*/protInfo.xml /home/eorchestra/election-orchestra/datastore/private/$1/*/publicKey_json $2 $3"
echo "> vmnd.sh Executing $COMMAND"
$COMMAND