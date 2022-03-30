#!/bin/bash

# This file is part of deployment-tool.
# Copyright (C) 2014-2016  Sequent Tech Inc <legal@sequentech.io>

# deployment-tool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# deployment-tool  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with deployment-tool.  If not, see <http://www.gnu.org/licenses/>.

# ./results.sh -t tally.tar.gz -c config.json -s

# fixes errors on non-ascii characters
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

SEQUENT_RESULTS=/home/eorchestra/tally-pipes
VENV=/home/eorchestra/renv
source $VENV/bin/activate
$SEQUENT_RESULTS/tally-pipes $*