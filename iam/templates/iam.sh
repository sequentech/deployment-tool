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

# https://stackoverflow.com/questions/9090683/supervisord-stopping-child-processes
# This kills the entire process group when the main script exits, such as when it is killed by supervisord.
# One of the processes that is usually left hanging is mixnet.
# Note that this is suposedly already handled by supervisor, but we do it also
# here just in case.
trap "kill -9 -- -$$" EXIT

uwsgi -b 32000 --ini /home/iam/uwsgi.ini
