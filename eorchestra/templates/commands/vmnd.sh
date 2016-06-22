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

EORCHESTRA=/home/eorchestra/
source $EORCHESTRA/.vfork_env
COMMAND="vmnd -i json /home/eorchestra/election-orchestra/datastore/private/$1/*/protInfo.xml /home/eorchestra/election-orchestra/datastore/private/$1/*/publicKey_json $2 $3"
echo "> vmnd.sh Executing $COMMAND"
$COMMAND
