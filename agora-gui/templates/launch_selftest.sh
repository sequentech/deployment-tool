#!/bin/bash

# This file is part of agora-dev-box.
# Copyright (C) 2022 Sequent Tech Inc <legal@sequentech.io>

# agora-dev-box is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# agora-dev-box  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with agora-dev-box.  If not, see <http://www.gnu.org/licenses/>.


function finish {
  echo "finishing"
  cat /home/agoragui/self_test_*.pid | xargs -I pid kill -9 pid
}
trap finish EXIT SIGINT

cd /home/agoragui/agora-gui-admin
grunt protractor
