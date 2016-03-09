#!/bin/bash
base=/home/agoragui
guib=/home/agoragui

# compile all the modules, one by one. stop if they don't build, because
# otherwise we would put in production a non-working version of the software
cd $guib/agora-gui-admin/
bower update --config.interactive=false
grunt build
if [ $? -ne 0 ]
then
  echo "build error in agora-gui-admin"
  exit 1
fi

cd $guib/agora-gui-booth/
bower update --config.interactive=false
grunt build
if [ $? -ne 0 ]
then
  echo "build error in agora-gui-booth"
  exit 1
fi

cd $guib/agora-gui-elections/
bower update --config.interactive=false
grunt build
if [ $? -ne 0 ]
then
  echo "build error in agora-gui-elections"
  exit 1
fi

# only switch to the new build if everything was built correctly
[ -d $base/dist-admin ] && rm -rf $base/dist-admin
cp -r $guib/agora-gui-admin/dist $base/dist-admin

[ -d $base/dist-booth ] && rm -rf $base/dist-booth
cp -r $guib/agora-gui-booth/dist $base/dist-booth

[ -d $base/dist-elections ] && rm -rf $base/dist-elections
cp -r $guib/agora-gui-elections/dist $base/dist-elections

[ -d $base/static_extra ] && ln -sf $guib/static_extra $base/dist-elections/static_extra