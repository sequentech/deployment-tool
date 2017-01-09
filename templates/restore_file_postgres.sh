#!/bin/bash

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

# Automatically exit bash on any error inside the exit
set -e

BACKUP_DIR={{ config.postgres_backups.folder }}
POSTGRES_DATA_DIR=/var/lib/postgresql/9.4/main

# check number of arguments
if [[ $# -ne 2 ]]; then
  echo "ERROR: invalid number of arguments: $#"
  exit 1
fi

FROM_PATH=$1
TO_PATH=$2

WHO=`whoami`
PRESENT_PATH=`pwd`

# check file exists
if [[ ! -f $BACKUP_DIR/wal/$FROM_PATH.gz ]]; then
  echo "ERROR: file $BACKUP_DIR/wal/$FROM_PATH.gz doesn't exist or is not a file. User: $WHO Path: $PRESENT_PATH . TO: $TO_PATH"
  exit 1
fi

gunzip < $BACKUP_DIR/wal/$FROM_PATH.gz > $TO_PATH
echo "extracted  $BACKUP_DIR/wal/$FROM_PATH.gz to $TO_PATH"

exit 0