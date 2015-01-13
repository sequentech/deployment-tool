#!/bin/bash

EORCHESTRA_DIR=/home/eorchestra

cd $EORCHESTRA_DIR/verificatum
sudo -u eorchestra make clean
# TODO: we need a real fix for this, in the future when we have more time..
rm verificatum/classes/verificatum/protocol/Protocol.class
rm verificatum/classes/verificatum/protocol/mixnet/MixNetElGamalInterfaceJSON.class
sudo -u eorchestra ./configure --enable-jgmpmee --enable-jecn
sudo -u eorchestra make
# fix wikstrom special o screwing things up
# http://stackoverflow.com/questions/361975/setting-the-default-java-character-encoding/623036#623036
# alternatively modify the makefile.am and makefile.in files
export JAVA_TOOL_OPTIONS=-Dfile.encoding=UTF8
make install
sudo -u eorchestra cp .verificatum_env /home/eorchestra
sudo -u eorchestra printf '\nsource /home/eorchestra/.verificatum_env' >> /home/eorchestra/.bashrc
sudo -u eorchestra -H bash -l -c "source /home/eorchestra/.verificatum_env && vog -rndinit RandomDevice /dev/urandom"
