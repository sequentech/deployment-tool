#!/bin/bash

found=$(grep '{{ config.private_ipaddress }} {{ config.host }}' /etc/hosts)
if [ $? -eq 1 ]
then
    echo "{{ config.private_ipaddress }} {{ config.host }}" >> /etc/hosts
fi
exists=$(su - postgres -c "psql -l | grep eorchestra | wc -l")
if [ $exists -ne 1 ]
then
        su - postgres -c "createuser -R -S -D eorchestra"
        su - postgres -c "createuser -s root"
        su - postgres -c "createdb -E utf-8 -O eorchestra eorchestra"
fi
