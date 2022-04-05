#!/usr/bin/python3

# This file is part of deployment-tool.
# Copyright (C) 2017  Sequent Tech Inc <legal@sequentech.io>

# deployment-tool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# deployment-tool  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with deployment-tool.  If not, see <http://www.gnu.org/licenses/>. 

import string
from os import urandom
import sys
import argparse
import re


# generate password with length number of characters
def gen_pass(length):
  alphabet = string.ascii_letters + string.digits
  return ''.join(alphabet[c % len(alphabet)] for c in urandom(length))

# read arguments
parser = argparse.ArgumentParser(description="Populate config.yml on deployment-tool with random passwords. WARNING: This WILL delete your passwords, please make a copy of config.yml before executing it.")
parser.add_argument('-c', '--config', help='Path to config.yml', default='config.yml')
parser.add_argument('-l', '--length', help='Passwords length, as number of characters (default: 22)', default=22, type=int)
parser.add_argument('-b', '--blank', help='Create a copy of config.yml with void passwords. Specify the path to the config.yml copy', default=False, action='store_true')
parser.add_argument('-o', '--out', help='Specify the path to the output config.yml', default=None)

args = parser.parse_args()

config_path = args.config
password_length = args.length
blank = args.blank
out_path = args.out

if out_path is None and not blank:
  out_path = config_path

# when setting the config.yml passwords to blank, the --out parameter is required
if out_path is None and blank:
  print('missing --out argument')
  exit(1)

out_text=""

with open(config_path, 'r', encoding='utf-8') as config_file_in:
  p = re.compile("(\s*)(backup_password|global_secret_key|eorchestra_password|db_password|shared_secret|keystore_pass|admin_password|password)\s*:\s('.*')(.*)")
  for line in config_file_in:
    newline = line
    if p.match(line):
      if blank:
        newline = p.sub(r"\1\2: ''\4", line)
      else:
        newline = p.sub(r"\1\2: '%s'\4" % gen_pass(password_length), line)
    out_text = out_text + newline

with open(out_path, 'w', encoding='utf-8') as config_file_out:
  config_file_out.seek(0)
  config_file_out.write(out_text)