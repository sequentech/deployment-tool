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

C={{ config.cert.C }}
ST={{ config.cert.ST }}
L={{ config.cert.L }}
O={{ config.cert.O }}
OU={{ config.cert.OU }}
HOST=${1:-`hostname`}
CN=${1:-`hostname`}
EMAIL={{ config.cert.EMAIL }}

cd /srv/certs/selfsigned/
CERT_PATH=/srv/certs/selfsigned/cert.pem

if [ ! -f $CERT_PATH ] || [ $(md5sum $CERT_PATH | grep 72a8ee2b40e77cd6e77e1db9285c7e19 | wc -l) == "1" ]
then
  openssl req -nodes -x509 -newkey rsa:4096 -keyout key-nopass.pem -out cert.pem -days {{config.cert.lifetime}} <<EOF
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

