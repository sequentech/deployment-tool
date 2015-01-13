#!/bin/bash

if [ ! "$(whoami)" == "root" ]
then
    echo "You need to execute this command as root"
    exit 1
fi

if [ ! -f $1 ]
then
    echo "$1 is not a file or cannot be read"
    exit 1
fi

export BACKUPD=/tmp/backup
export EO_DIR=/home/eorchestra/election-orchestra/
rm -rf $BACKUPD
cd $(dirname $BACKUPD)
rm -rf tmp.tar.gz

PASSWORD=$(cat /root/.backup_password)
gpg --passphrase "$PASSWORD" -o tmp.tar.gz -d $1  2>/dev/null
tar zxf tmp.tar.gz
rm tmp.tar.gz

cd $BACKUPD

supervisorctl stop eorchestra
service nginx stop

cp -rpxf $BACKUPD/certs/* /srv/certs/
cp /srv/certs/selfsigned/* /home/eorchestra/election-orchestra/certs/selfsigned/
cp $BACKUPD/eo_base_settings.py $EO_DIR/eo_base_settings.py
# cp $BACKUPD/eo_db.sqlite $EO_DIR/db.sqlite
# backup existing just in case
su - orchestra -c "pg_dump eorchestra" > /tmp/eo_pre_restore_db.sql
# restore
su - postgres -c "dropdb eorchestra"
su - postgres -c "createdb -E utf-8 -O eorchestra eorchestra"
su - postgres -c "psql eorchestra < $BACKUPD/eo_db.sql"

if [ ! -d $EO_DIR/datastore/private/ ]
then
    mkdir -p $EO_DIR/datastore/private/
    chown eorchestra:users $EO_DIR/datastore/private/
fi

if [ -d $BACKUPD/eo_private/ ]
then
    cp -rpxf $BACKUPD/eo_private/* $EO_DIR/datastore/private/
fi

if [ ! -d /srv/election-orchestra/server1/public/ ]
then
    mkdir -p /srv/election-orchestra/server1/public/
    chown eorchestra:users /srv/election-orchestra/server1/public/
fi

if [ -d  $BACKUPD/eo_public/ ]
then
    cp -rpxf $BACKUPD/eo_public/* /srv/election-orchestra/server1/public/
fi

if [ ! -d /etc/eopeers/ ]
then
    mkdir -p /etc/eopeers/
fi
if [ -d $BACKUPD/eo_peers/ ]
then
    cp -rpxf $BACKUPD/eo_peers/* /etc/eopeers/
    eopeers --install /etc/eopeers/*
fi

cp $BACKUPD/hosts /etc/hosts
cp $BACKUPD/nginx_conf/* /etc/nginx/conf.d
cp $BACKUPD/supervisor_confd/* /etc/supervisor/conf.d

# we do not restore logs, that's just stored for analysis


cd
rm -rf $BACKUPD

supervisorctl start eorchestra
service nginx start