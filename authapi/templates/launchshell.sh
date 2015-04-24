#!/bin/bash
source ~/env/bin/activate
cd ~/authapi/authapi
./manage.py shell --settings=authapi.deploy