#!/bin/bash

# This file is part of deployment-tool.
# Copyright (C) 2022 Sequent Tech Inc <legal@sequentech.io>

# deployment-tool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# deployment-tool  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with deployment-tool.  If not, see <http://www.gnu.org/licenses/>.

function finish {
  echo "finishing"
  cat /home/iam/celery_beat_*.pid | xargs -I pid kill -9 pid
}
trap finish EXIT SIGINT

DJANGO_SETTINGS_MODULE='iam.deploy' /home/iam/env/bin/celery \
  -A iam \
  beat \
  --pidfile '/home/iam/celery_beat_%n.pid' \
  {{ config.iam.celery_beat_extra_opts }}
