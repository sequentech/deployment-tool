#!/bin/bash
base=/home/agoragui
guib=/home/agoragui

rm -rf $base/dist-admin
rm -rf $base/dist-booth
rm -rf $base/dist-elections

cd $guib/agora-gui-admin/
grunt build && cp -r dist $base/dist-admin

cd $guib/agora-gui-booth/
grunt build && cp -r dist $base/dist-booth

cd $guib/agora-gui-elections/
grunt build && cp -r dist $base/dist-elections
