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

base=/home/agoragui
guib=/home/agoragui

TASK=$1

{% if config.has_https_proxy %}
# otherwise bower won't use the proxy appropiately
export https_proxy=$http_proxy
{% endif %}

# compile all the modules, one by one. stop if they don't build, because
# otherwise we would put in production a non-working version of the software
if {[ -z $TASK ] || test "$TASK" = "admin" }
then
  cd $guib/agora-gui-admin/
  yarn --non-interactive && grunt build
  if [ $? -ne 0 ]
  then
    echo "build error in agora-gui-admin"
    exit 1
  fi
fi

if {[ -z $TASK ] || test "$TASK" = "booth" }
then
  cd $guib/agora-gui-booth/
  yarn --non-interactive && grunt build
  if [ $? -ne 0 ]
  then
    echo "build error in agora-gui-booth"
    exit 1
  fi
fi

if {[ -z $TASK ] || test "$TASK" = "elections" }
then
  cd $guib/agora-gui-elections/
  yarn --non-interactive && grunt build
  if [ $? -ne 0 ]
  then
    echo "build error in agora-gui-elections"
    exit 1
  fi
fi

# only switch to the new build if everything was built correctly
if {[ -z $TASK ] || test "$TASK" = "admin" }
then
  [ -d $base/dist-admin ] && rm -rf $base/dist-admin
  cp -r $guib/agora-gui-admin/dist $base/dist-admin
fi

if {[ -z $TASK ] || test "$TASK" = "booth" }
then
  [ -d $base/dist-booth ] && rm -rf $base/dist-booth
  cp -r $guib/agora-gui-booth/dist $base/dist-booth
fi

if {[ -z $TASK ] || test "$TASK" = "elections" }
  [ -d $base/dist-elections ] && rm -rf $base/dist-elections
  cp -r $guib/agora-gui-elections/dist $base/dist-elections
then

[ -d $base/static_extra ] && cp -r $guib/static_extra $base/dist-elections/static_extra || true
