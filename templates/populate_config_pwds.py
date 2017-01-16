#!/usr/bin/python

# This file is part of agora-dev-box.
# Copyright (C) 2017  Agora Voting SL <agora@agoravoting.com>

# agora-dev-box is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# agora-dev-box  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with agora-dev-box.  If not, see <http://www.gnu.org/licenses/>. 

# if ruamel.yaml is not installed, execute:
# $ sudo pip install ruamel.yaml

# first argument is the path to config.yml, otherwise it's assumed it's on path ./config.yml

import ruamel.yaml
import string
from os import urandom
from ruamel.yaml.scalarstring import SingleQuotedScalarString, DoubleQuotedScalarString
import sys

def gen_pass():
  length = 22
  alphabet = string.ascii_letters + string.digits
  return SingleQuotedScalarString(''.join(alphabet[c % len(alphabet)] for c in urandom(length)))

config_path = 'config.yml'

# read paths from the arguments
if 2 <= len(sys.argv):
    config_path = sys.argv[1]


with open(config_path, 'r', encoding='utf-8') as config_file_in:
  code = ruamel.yaml.round_trip_load(config_file_in.read(), preserve_quotes=True)

code['config']['backup_password'] = gen_pass()
code['config']['global_secret_key'] = gen_pass()
code['config']['eorchestra_password'] = gen_pass()
code['config']['agora_elections']['db_password'] = gen_pass()
code['config']['agora_elections']['shared_secret'] = gen_pass()
code['config']['agora_elections']['keystore_pass'] = gen_pass()
code['config']['sentry']['db_password'] = gen_pass()
code['config']['sentry']['admin_password'] = gen_pass()
code['config']['authapi']['admin_user']['password'] = gen_pass()

out_text = ruamel.yaml.round_trip_dump(code, Dumper=ruamel.yaml.RoundTripDumper)

with open(config_path, 'w', encoding='utf-8') as config_file_out:
  config_file_out.seek(0)
  config_file_out.write(out_text)