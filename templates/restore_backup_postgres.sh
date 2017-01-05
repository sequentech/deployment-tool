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
# https://www.postgresql.org/docs/9.4/static/continuous-archiving.html#BACKUP-BASE-BACKUP point 24.3.4
# 
# basic steps:
# 1: make a copy of /var/lib/postgresql/9.4/main
# 2: remove /var/lib/postgresql/9.4/main
# 3: unzip base backup from /home/eorchestra/postgres_backups/base/whatever and copy it to /var/lib/postgresql/9.4/main
# 4: unzip wal files from  /home/eorchestra/postgres_backups/wal to a folder F_WAL
# 5: copy /etc/postgresql/9.4/main/recovery.conf to the data folder: /var/lib/postgresql/9.4/main/recovery.conf
# 6: edit restore_command variable from recovery.conf to copy files from F_WAL, edit recovery_target_time if you want recover up to a specific date
# 7: restart postgres