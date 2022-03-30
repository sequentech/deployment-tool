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

base=/home/ui_user
guib=/home/ui_user

TASK=$1

{% if config.has_https_proxy %}
# otherwise bower won't use the proxy appropiately
export https_proxy=$http_proxy
{% endif %}

# compile all the modules, one by one. stop if they don't build, because
# otherwise we would put in production a non-working version of the software
if [ -z $TASK ] || test "$TASK" = "admin"
then
  echo "Building admin-console.."
  cd $guib/admin-console/
  yarn --non-interactive && grunt build
  if [ $? -ne 0 ]
  then
    echo "build error in admin-console"
    exit 1
  fi
elif [ -z $TASK ] || test "$TASK" = "booth"
then
  echo "Building voting-booth.."
  cd $guib/voting-booth/
  yarn --non-interactive && grunt build
  if [ $? -ne 0 ]
  then
    echo "build error in voting-booth"
    exit 1
  fi
elif [ -z $TASK ] || test "$TASK" = "elections"
then
  echo "Building election-portal.."
  cd $guib/election-portal/
  yarn --non-interactive && grunt build
  if [ $? -ne 0 ]
  then
    echo "build error in election-portal"
    exit 1
  fi
else 
  echo "Invalid task to build: $TASK"
  exit 1
fi

# only switch to the new build if everything was built correctly
if [ -z $TASK ] || test "$TASK" = "admin"
then
  echo "Deploying admin-console.."
  [ -d $base/dist-admin ] && rm -rf $base/dist-admin
  cp -r $guib/admin-console/dist $base/dist-admin
fi

if [ -z $TASK ] || test "$TASK" = "booth"
then
  echo "Deploying voting-booth.."
  [ -d $base/dist-booth ] && rm -rf $base/dist-booth
  cp -r $guib/voting-booth/dist $base/dist-booth
fi

if [ -z $TASK ] || test "$TASK" = "elections"
then
  echo "Deploying election-portal.."
  [ -d $base/dist-elections ] && rm -rf $base/dist-elections
  cp -r $guib/election-portal/dist $base/dist-elections
fi

[ -d $base/static_extra ] && cp -r $guib/static_extra $base/dist-elections/static_extra || true
