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
  echo "copy_wall_postgress input ERROR: invalid number of arguments:" $#
  exit 1
fi

# check first argument is an existing folder
if [[ ! -d $1 ]]; then
  echo "argument" $1 "is not an existing folder"
  exit 1
fi

# check second argument is an existing file
if [[ ! -f $1/$2 ]]; then
  echo "argument" $2 "is not an existing file on folder" $1
  exit 1
fi

FROM_PATH=$1
FILE_NAME=$2
TO_PATH={{ backups.folder }}/wal

# check whether wal folder exists
if [[ ! -d $TO_PATH ]]; then
  echo "wal folder $TO_PATH does not exist"
  exit 1
fi

tar -czf $TO_PATH/$FILE_NAME.tar.gz $FROM_PATH/$FILE_NAME