#!/bin/bash

C=ES
ST=Madrid
L=Madrid
O=Agoravoting
OU=Agora_Voting_SL
HOST=${1:-`hostname`}
CN=${1:-`hostname`}
EMAIL=agora@agoravoting.com

cd /srv/certs/selfsigned/
CERT_PATH=/srv/certs/selfsigned/cert.pem

if [ ! -f $CERT_PATH ] || [ $(md5sum $CERT_PATH | grep 72a8ee2b40e77cd6e77e1db9285c7e19 | wc -l) == "1" ]
then
  openssl req -nodes -x509 -newkey rsa:4096 -keyout key-nopass.pem -out cert.pem -days 365 <<EOF
${C}
${ST}
${L}
${O}
${OU}
${CN}
${EMAIL}
EOF
  cp cert.pem calist
fi
