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

# NOTE:
# in order to recover, use this information:
# https://www.postgresql.org/docs/12/static/continuous-archiving.html#BACKUP-BASE-BACKUP point 24.3.4
# 
# basic steps:
# 0: stop postgresql service
# 1: make a copy of /var/lib/postgresql/12/main
# 2: remove /var/lib/postgresql/12/main
# 3: unzip base backup from /home/eorchestra/postgres_backups/base/whatever and copy it to /var/lib/postgresql/12/main
# 4: unzip wal files from  /home/eorchestra/postgres_backups/wal to a folder F_WAL
# 5: copy /etc/postgresql/12/main/recovery.conf.copy to the data folder: /var/lib/postgresql/12/main/recovery.conf
# 6: edit restore_command variable from recovery.conf to copy files from F_WAL, edit recovery_target_time if you want recover up to a specific date
# 7: start postgres

# Automatically exit bash on any error inside the exit
set -e

BACKUP_DIR={{ config.postgres_backups.folder }}
DATE=`date '+%d_%m_%y_%H_%M_%S'`
POSTGRES_DATA_DIR=/var/lib/postgresql/12/main
POSTGRES_CONFIG_DIR=/etc/postgresql/12/main

function print_help {
  echo -e """usage: restore_backups_postgres.sh [base-backup] [date]

Restores the PostgreSQL database to a previous state. Execute the command as root.

  [base-backup]\tName of the base backup (can be dump or continuous archiving). Required
  [date]       \tRecover the database as it was at a given date. Optional, only for continuous archiving
  """
}

if [[ $# -lt 1 ]]; then
  echo "ERROR: argument 1 (base backup name) missing"
  print_help
  exit 1
fi

BASE_BACKUP_NAME=$1

# The user executing the script needs be root
if [ ! "$(whoami)" == "root" ]; then
  echo "ERROR: You need to execute this command as root"
  exit 1
fi

if [ "$BASE_BACKUP_NAME" == "dump" ]; then
  echo "ERROR: invalid argument: $BASE_BACKUP_NAME"
  exit 1
fi

# check if we want to restore a dump backup
DUMP_TEST=`echo $BASE_BACKUP_NAME | sed 's/dump_.*/dump/'`

# dump backup
if [ "$DUMP_TEST" == "dump" ]; then
  # check whether base backup exists
  if [[ ! -f $BACKUP_DIR/dump/$BASE_BACKUP_NAME.gz ]]; then
    echo "ERROR: base backup file missing (or it's not a file): $BACKUP_DIR/dump/$BASE_BACKUP_NAME.gz"
    exit 1
  fi
  # stop postgresql
  echo "Stopping postgresql service..."
  service postgresql stop 12
  echo "Stopped"

  # check whether postgres data_directory exists and make backup
  if [[ -d $POSTGRES_DATA_DIR ]]; then
    echo "Creating backup of existing PostgreSQL data directory"
    if [[ ! -d $BACKUP_DIR/restore_backups ]]; then
      sudo -u postgres mkdir $BACKUP_DIR/restore_backups
    fi
    sudo -u postgres tar -zcvf $BACKUP_DIR/restore_backups/$DATE.tar.gz $POSTGRES_DATA_DIR
    echo "Created"
  else
    echo "PostgreSQL data directory doesn't exist yet so we don't need to make a backup"
  fi

  # create copy of cluster configuration
  tar -C $POSTGRES_CONFIG_DIR -zcvf $BACKUP_DIR/dump/$BASE_BACKUP_NAME.cfg.tar.gz .

  # HACK: FIXME
  # restoring a dump sql backup by the means we are using (dropping and 
  # creating the cluster from scratch) means timeline will be  set to 1. This
  # can generate problems for WAL backups, so we move all the wal backups to a
  # subfolder
  if ls $BACKUP_DIR/wal/*.gz &> /dev/null; then
    mkdir $BACKUP_DIR/wal/$DATE
    mv $BACKUP_DIR/wal/*.gz $BACKUP_DIR/wal/$DATE
    chown postgres:postgres -R $BACKUP_DIR/wal/$DATE
  fi

  # unzip
  echo "Unzipping backup.."
  gunzip < $BACKUP_DIR/dump/$BASE_BACKUP_NAME.gz > $BACKUP_DIR/dump/$BASE_BACKUP_NAME.sql
  chown postgres:postgres $BACKUP_DIR/dump/$BASE_BACKUP_NAME.sql
  echo "Unzipped"

  echo "Recreating cluster"
  # Remove whole cluster
  pg_dropcluster 12 main
  pg_createcluster 12 main
  pg_ctlcluster 12 main start
  # Recover cluster config
  service postgresql stop 12
  tar -C $POSTGRES_CONFIG_DIR -zxvf $BACKUP_DIR/dump/$BASE_BACKUP_NAME.cfg.tar.gz .
  service postgresql start 12
  sudo -u postgres psql -f $BACKUP_DIR/dump/$BASE_BACKUP_NAME.sql > /dev/null
  echo "Cluster successfully recreated"

  echo "Removing temporary data"
  rm -R $BACKUP_DIR/dump/$BASE_BACKUP_NAME.sql $BACKUP_DIR/dump/$BASE_BACKUP_NAME.cfg.tar.gz
  echo "Temporary data removed"

# continuous archiving WAL backup
else
  # check whether base backup exists
  if [[ ! -d  $BACKUP_DIR/base/$BASE_BACKUP_NAME ]]; then
    echo "ERROR: base backup folder missing (or it's not a folder): $BACKUP_DIR/base/$BASE_BACKUP_NAME"
    exit 1
  elif [[ ! -f $BACKUP_DIR/base/$BASE_BACKUP_NAME/base.tar.gz ]]; then
    echo "ERROR: base backup file missing (or it's not a file): $BACKUP_DIR/base/$BASE_BACKUP_NAME/base.tar.gz"
    exit 1
  fi

  # stop postgresql
  echo "Stopping postgresql service..."
  service postgresql stop 12
  echo "Stopped"

  # check whether postgres data_directory exists and make backup
  if [[ -d $POSTGRES_DATA_DIR ]]; then
    echo "Creating backup of existing PostgreSQL data directory"
    if [[ ! -d $BACKUP_DIR/restore_backups ]]; then
      sudo -u postgres mkdir $BACKUP_DIR/restore_backups
    fi
    sudo -u postgres tar -zcvf $BACKUP_DIR/restore_backups/$DATE.tar.gz $POSTGRES_DATA_DIR
    sudo -u postgres rm -Rf $POSTGRES_DATA_DIR
    echo "Created"
  else
    echo "PostgreSQL data directory doesn't exist yet so we don't need to make a backup"
  fi

  # restore backup
  mkdir $POSTGRES_DATA_DIR
  tar -zxvf $BACKUP_DIR/base/$BASE_BACKUP_NAME/base.tar.gz -C $POSTGRES_DATA_DIR
  cp $POSTGRES_CONFIG_DIR/recovery.conf.copy $POSTGRES_DATA_DIR/recovery.conf

  # set backup date
  if [[ $# -ge 2 ]]; then
    BACKUP_DATE=$2 # e.g. '2004-07-14 22:39:00 EST'
    RECOVERY_CONF=`cat $POSTGRES_DATA_DIR/recovery.conf | sed -r "s/\s*#?\s*recovery_target_time\s*=\s*'.*'(.*)/recovery_target_time = '$BACKUP_DATE'\1/"`
    echo "$RECOVERY_CONF" > $POSTGRES_DATA_DIR/recovery.conf
  fi
  chown postgres.postgres -R $POSTGRES_DATA_DIR
  chmod 0700 -R $POSTGRES_DATA_DIR

  # start postgresql to restore the backup
  service postgresql start 12
fi

echo "Backup restored"
exit 0
