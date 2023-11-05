#!/bin/bash

# This file is part of deployment-tool.
# Copyright (C) 2017 Sequent Tech Inc <legal@sequentech.io>

# deployment-tool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# deployment-tool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with deployment-tool. If not, see <http://www.gnu.org/licenses/>.

# Automatically exit bash on any error inside the exit
set -e

BACKUP_DIR={{ config.postgres_backups.folder }}
KEEP_DAYS={{ config.postgres_backups.base_backups.keep_days }}
DATE_NOW=$(date +%s)

if [ "$KEEP_DAYS" -eq "0" ]; then
  echo "keeping backups indefinitely"
  exit 0
fi

DATE_OLDEST=$(echo "$DATE_NOW - (24*3600*$KEEP_DAYS)" | bc)

delete_old_files() {
  local directory=$1
  local list=$2

  for FNAME in $list; do
    # Get file's last modification time in seconds since the epoch
    local FDATE=$(date -r "$directory/$FNAME" +%s)

    # check date and remove if it's too old
    if [ "$DATE_OLDEST" -gt "$FDATE" ]; then
      local full_path="$directory/$FNAME"
      echo "deleting $full_path"
      rm -rf "$full_path"
    fi
  done
}

LIST_BASE=$(ls "$BACKUP_DIR/base")
LIST_DUMP=$(ls "$BACKUP_DIR/dump")
LIST_WAL=$(ls "$BACKUP_DIR/wal")

delete_old_files "$BACKUP_DIR/base" "$LIST_BASE"
delete_old_files "$BACKUP_DIR/dump" "$LIST_DUMP"
delete_old_files "$BACKUP_DIR/wal" "$LIST_WAL"

exit 0
