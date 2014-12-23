#!/bin/bash

EORCHESTRA_DIR=/home/eorchestra
VENV_DIR=$EORCHESTRA_DIR/venv

git config --global user.email "you@example.com"
git config --global user.name "Your Name"

cd $EORCHESTRA_DIR 
git clone https://github.com/agoravoting/frestq
git clone https://github.com/agoravoting/election-orchestra
source $VENV_DIR/bin/activate
pip install setuptools==2.2
cd $EORCHESTRA_DIR/frestq
python setup.py install
cd $EORCHESTRA_DIR/election-orchestra
pip install -r requirements.txt
cp -f /tmp/base_settings.py base_settings.py
export FRESTQ_SETTINGS=base_settings.py 
python app.py --createdb

C=ES
ST=Madrid
L=Madrid
O=Agoravoting
OU=Agora_Voting_SL
HOST=${1:-`hostname`}
CN=${1:-`hostname`}
EMAIL=agora@agoravoting.com

cd $EORCHESTRA_DIR/election-orchestra/certs/selfsigned/
CERT_PATH=$EORCHESTRA_DIR/election-orchestra/certs/selfsigned/cert.pem

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


