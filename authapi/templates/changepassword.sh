#!/usr/bin/expect


set user [lindex $argv 0]
set key [lindex $argv 1]

spawn ~/launchcommand.sh "./manage.py changepassword ${user} --settings=authapi.deploy"
expect "*Password*"
send "${key}\n"
expect "*Password*"
send "${key}\n"
expect "*Password*"
send "\n"