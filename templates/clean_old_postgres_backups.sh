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
KEEP_DAYS={{ config.postgres_backups.base_backups.keep_days }}
DATE_NOW=`date +%s`

if [ "$KEEP_DAYS" -eq "0" ]; then
  echo "keeping backups indefinitely"
  exit 0
fi

DATE_OLDEST=`echo "$DATE_NOW - (24*3600*$KEEP_DAYS)" | bc`

LIST_BASE=`ls $BACKUP_DIR/base`
LIST_DUMP=`ls $BACKUP_DIR/dump`

for FNAME in $LIST_BASE
do
  RAW_DATE=`echo $FNAME | sed 's/\([[:digit:]]*\)_\([[:digit:]]*\)_\([[:digit:]]*\)_\([[:digit:]]*\)_\([[:digit:]]*\)_\([[:digit:]]*\)/20\3-\2-\1 \4:\5:\6/'`
  if [ "$RAW_DATE" == "$FNAME" ]; then
    continue
  fi
  FDATE=`date --date="$RAW_DATE" +%s`

  # check date and remove if it's too old
  if [ "$DATE_OLDEST" -gt "$FDATE" ]; then
    echo "deleting $BACKUP_DIR/base/$FNAME"
    rm -Rf $BACKUP_DIR/base/$FNAME
  fi
done

for FNAME in $LIST_DUMP
do
  RAW_DATE=`echo $FNAME | sed 's/dump_\([[:digit:]]*\)_\([[:digit:]]*\)_\([[:digit:]]*\)_\([[:digit:]]*\)_\([[:digit:]]*\)_\([[:digit:]]*\)\.gz/20\3-\2-\1 \4:\5:\6/'`
  if [ "$RAW_DATE" == "$FNAME" ]; then
    continue
  fi
  FDATE=`date --date="$RAW_DATE" +%s`

  # check date and remove if it's too old
  if [ "$DATE_OLDEST" -gt "$FDATE" ]; then
    echo "deleting $BACKUP_DIR/base/$FNAME"
    rm -Rf $BACKUP_DIR/base/$FNAME
  fi
done

exit 0