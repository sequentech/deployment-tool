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

# The user executing the script needs be root
if [ ! "$(whoami)" == "root" ]
then
  echo "You need to execute this command as root"
  exit 1
fi

BACKUP_DIR={{ config.postgres_backups.folder }}
DATE=`date '+%d_%m_%y_%H_%M_%S'`

pg_basebackup -U postgres -x --format=tar --gzip --compress=9 -D $BACKUP_DIR/base/$DATE
echo "base backup created on $BACKUP_DIR/base/$DATE" | logger -t backup_cron_postgres

sudo -u postgres pg_dumpall | tee $BACKUP_DIR/dump/dump_$DATE;
gzip < $BACKUP_DIR/dump/dump_$DATE > $BACKUP_DIR/dump/dump_$DATE.gz
rm $BACKUP_DIR/dump/dump_$DATE
echo "dump backup created on $BACKUP_DIR/dump/dump_$DATE.gz" | logger -t backup_cron_postgres
