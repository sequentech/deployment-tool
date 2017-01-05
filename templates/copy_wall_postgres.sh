#!/bin/bash

# This file is part of agora-dev-box.
# Copyright (C) 2016-2017  Agora Voting SL <agora@agoravoting.com>

# agora-dev-box is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# agora-dev-box  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with agora-dev-box.  If not, see <http://www.gnu.org/licenses/>.

# Automatically exit bash on any error inside the exit
set -e

# check number of arguments
if [[ $# -ne 2 ]]; then
  echo "ERROR: invalid number of arguments: $#"
  exit 1
fi

FROM_PATH=$1
FILE_NAME=$2
TO_PATH={{ config.postgres_backups.folder }}/wal

# check first argument is an existing file
if [[ ! -f $FROM_PATH ]]; then
  echo "ERROR: argument $FROM_PATH is not an existing file"
  exit 1
fi

# check whether wal folder exists
if [[ ! -d $TO_PATH ]]; then
  echo "ERROR: wal folder $TO_PATH does not exist"
  exit 1
fi

# check whether wal file already exists
if [[ -f $TO_PATH/$FILE_NAME.gz ]]; then
  echo "ERROR: wal archive file $TO_PATH/$FILE_NAME.gz already exists and shouldn't be overwritten"
  exit 1
fi

gzip < $FROM_PATH > $TO_PATH/$FILE_NAME.gz
echo "copied $FROM_PATH to $TO_PATH/$FILE_NAME.gz"
exit 0