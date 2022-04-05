#!/usr/bin/expect

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

set user [lindex $argv 0]
set key [lindex $argv 1]

spawn ~/launchcommand.sh "./manage.py changepassword ${user} --settings=iam.deploy"
expect "*Password*"
send "${key}\n"
expect "*Password*"
send "${key}\n"
expect "*Password*"
send "\n"