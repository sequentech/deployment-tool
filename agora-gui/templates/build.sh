#!/bin/bash
base=/home/agoragui
guib=/home/agoragui

# compile all the modules

cd $guib/agora-gui-admin/
grunt build || (echo "build error in agora-gui-admin" && exit 1)

cd $guib/agora-gui-booth/
grunt build || (echo "build error in agora-gui-booth" && exit 1)

cd $guib/agora-gui-elections/
grunt build || (echo "build error in agora-gui-elections" && exit 1)

# only switch to the new build if everything was built correctly

rm -rf $base/dist-admin && cp -r guib/agora-gui-admin/dist $base/dist-admin
rm -rf $base/dist-booth && cp -r guib/agora-gui-booth/dist $base/dist-booth
rm -rf $base/dist-elections && cp -r guib/agora-gui-elections/dist $base/dist-elections
