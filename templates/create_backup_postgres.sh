#!/bin/bash

# This file is part of agora-dev-box.
# Copyright (C) 2016  Agora Voting SL <agora@agoravoting.com>

# agora-dev-box is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# agora-dev-box  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with agora-dev-box.  If not, see <http://www.gnu.org/licenses/>. 

# The user executing the script needs be root
if [ ! "$(whoami)" == "root" ]
then
  echo "You need to execute this command as root"
  exit 1
fi

BACKUP_DIR={{ backups.dir }}
DATE=`date '+%d_%m_%y_%H_%M_%S'`

pg_basebackup -x --format=tar --gzip --compress=9 -D $BACKUP_DIR/base/$DATE

pg_dumpall | gzip > $BACKUP_DIR/dump/dump_$DATE.gz