#!/bin/bash

# This file is part of agora-dev-box.
# Copyright (C) 2014-2016  Agora Voting SL <agora@agoravoting.com>

# agora-dev-box is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# agora-dev-box  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with agora-dev-box.  If not, see <http://www.gnu.org/licenses/>.

HOME=/home/eorchestra

source $HOME/venv/bin/activate
export FRESTQ_SETTINGS="base_settings.py"

# https://stackoverflow.com/questions/9090683/supervisord-stopping-child-processes
# This kills the entire process group when the main script exits, such as when it is killed by supervisord.
# One of the processes that is usually left hanging is vfork.
# Note that this is suposedly already handled by supervisor, but we do it also
# here just in case.
trap "kill -9 -- -$$" EXIT

$HOME/venv/bin/uwsgi --ini $HOME/election-orchestra/auth.ini
