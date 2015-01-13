#!/bin/bash

if [ ! "$(whoami)" == "root" ]
then
  echo "You need to execute this command as root"
  exit 1
fi

BACKUPD=/tmp/backup
BACKUP_DIR=/backup
EO_DIR=/home/eorchestra/election-orchestra/
DATE=`date '+%d_%m_%y_%H_%M'`

rm -rf $BACKUPD
mkdir -p $BACKUPD
cd $BACKUPD

[ -d $BACKUP_DIR ] || mkdir $BACKUP_DIR

supervisorctl stop eorchestra

cp -rpxf /srv/certs/ $BACKUPD/certs
cp $EO_DIR/base_settings.py $BACKUPD/eo_base_settings.py
# cp $EO_DIR/db.sqlite $BACKUPD/eo_db.sqlite
su - eorchestra -c "pg_dump eorchestra" > $BACKUPD/eo_db.sql

if [ ! $(ls /srv/election-orchestra/server1/public/ | wc -l) -eq "0" ]
then
    cp -rpxf /srv/election-orchestra/server1/public/ $BACKUPD/eo_public
fi

if [ ! $(ls $EO_DIR/datastore/private/ | wc -l) -eq "0" ]
then
    cp -rpxf $EO_DIR/datastore/private $BACKUPD/eo_private
fi

if [ -d /etc/eopeers ] && [ ! $(ls /etc/eopeers/ | wc -l) -eq "0" ]
then
    cp -rpxf /etc/eopeers $BACKUPD/eo_peers
fi

cp /etc/hosts $BACKUPD/hosts
cp -rpxf /etc/nginx/conf.d $BACKUPD/nginx_conf
cp -rpxf /etc/supervisor/conf.d $BACKUPD/supervisor_confd
mkdir $BACKUPD/logs
cp /var/log/auth.* $BACKUPD/logs
cp /var/log/dmesg.* $BACKUPD/logs
cp -r /var/log/supervisor $BACKUPD/logs/supervisor
cp -r /var/log/nginx $BACKUPD/logs/nginx

supervisorctl start eorchestra

BACKUP="${BACKUP_DIR}/${DATE}.tar.gz"
cd $(dirname $BACKUPD)
tar zcf "${BACKUP_DIR}/${DATE}.tar.gz" $(basename $BACKUPD)

PASSWORD=$(cat /root/.backup_password)

gpg --passphrase "$PASSWORD" -c $BACKUP 2>/dev/null
rm $BACKUP


[ -f $BACKUP_DIR/latest ] && rm $BACKUP_DIR/latest
ln -sf "$BACKUP.gpg" $BACKUP_DIR/latest

