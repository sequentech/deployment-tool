#!/usr/bin/python3

# This file is part of deployment-tool.
# Copyright (C) 2016-2020  Sequent Tech Inc <legal@sequentech.io>

# deployment-tool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# deployment-tool  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with deployment-tool.  If not, see <http://www.gnu.org/licenses/>.

import sys

# The aim of this small script is to remove a certificate from a list of
# certificates. The result is printed in the standard output.

cert_path = "{{ config.http.tls_cert_path }}"
calist_path = "{{ config.http.tls_calist_path }}"

# read paths from the arguments
if 3 == len(sys.argv):
    cert_path = sys.argv[1]
    calist_path = sys.argv[2]

# read cert
cert_file = open(cert_path, "r")
started = False
ended = False
cert = ""
for line in cert_file:
    if started and not ended:
        cert = cert + line
        if "-----END CERTIFICATE-----" in line:
            ended = True
    elif not started and not ended:
        if "-----BEGIN CERTIFICATE-----" in line:
            cert = cert + line
            started = True
cert_file.close()

# store calist file in a single string
calist_file = open(calist_path, "r")
calist = calist_file.read()
calist_file.close()

# remove cert from calist
calist2 = calist.replace(cert, "")

# print to standard output
print calist2
