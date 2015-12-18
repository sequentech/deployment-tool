# Complete Agora Voting production deployment system

This document describes the complete deployment of an Agora Voting system
with two Authorities for a production environment in virtual machines with
reduced root priviledges.

## Requirements

You need 4 Linux x64 host machines with at least 3GB of RAM each and a clean
Ubuntu  14.04 LTS installed. We will make a deployment with limited root
permisssions.

The structure of the four machines is:

- agora1
  used as master web server

- agora2
  used as slave web server

- auth1
  used as election authority 1

- auth2
  used as election authority 2

The instructions in the requirements section should be executed in all 4
machines. We asume that either:

a. another fith machine will be used as the load balancer and for high
availability purposes and act as the public interface to the Internet.

b. agora1 will be used as the public interface interface to the Internet unless
it fails, then agora2 will be used for that as a redundancy strategy.

- Configure permissions

First, create the deployment user if it hasn't been created yet. We'll use
**agora** for that:

    root@agora # adduser agora agora

Afterwards, you should add the permissions that the agora user requires for
administration and deployment.

This is how you do it in the two servers that will be used as authorities:

    root@agora # wget https://github.com/agoravoting/agora-dev-box/blob/feature_load_balancing_high_availability/doc/production/auth.sudoers
    root@agora # cat auth.sudoers >> /etc/sudoers

And this is how you do it for the two other servers that will be used as master
and slave machines:

    root@agora # wget https://github.com/agoravoting/agora-dev-box/blob/feature_load_balancing_high_availability/doc/production/auth.sudoers
    root@agora # cat auth.sudoers >> /etc/sudoers

- Install initial dependencies

Once permissions have been granted, we'll continue to execute everything through
the **agora** user. Now We need to install some requirements needed to continue:

    agora@agora:~ $ sudo apt-get install software-properties-common pwgen
    agora@agora:~ $ sudo apt-add-repository ppa:ansible/ansible -y
    agora@agora:~ $ sudo apt-get update
    agora@agora:~ $ sudo apt-get install -y ansible git

- Configure ports and permissions

The 4 machines should be visible one to the other, and firewall rules should be
created to allow the following kind of connections:

-  agora1 <<tcp:5432>> agora2 # postgresql
-  agora1 <<tcp:22>> agora2 # rsync
-  [agora1, agora2] <<tcp:443>> Internet # web service
-  [agora1, agora2] <<tcp:9090>> Internet # sentry
-  auth1 <<tcp:5000>> auth2 # eotest
-  auth1 <<tcp:4081>> auth2 # verificatum
-  auth1 <<udp:8081>> auth2 # verificatum

# Agora web servers master deployment [agora1, agora2]

The following steps should be executed in both web servers. Download the
deployment script:

    agora@agora:~ $ git clone https://github.com/agoravoting/agora-dev-box.git
    agora@agora:~ $ cd agora-dev-box
    agora@agora:~/agora-dev-box/ $ git checkout feature_load_balancing_high_availability

We'll use a master config file as a base:

    agora@agora:~/agora-dev-box/ $ cp doc/production/config.master.yml config.yml

Then edit the base configuration file **config.yml**. Change all the
'<PASSWORD>' to specific passwords. You can generate 20 password
with 20 cahracters each with the following command:

    agora@agora $ pwgen 20 20

Both machines agora1 and agora2 should be setup with the same passwords,
because they will be a replica of each other: the slave will be in hot standby
configuration. The only difference between the configuration file of **agora1**
and **agora2** should be the following config keys:

* config.host
* config.public_ipaddress
* config.private_ipaddress
* config.load_balancing.repmgr_node_id

Please read the comments and instructions inside the configuration file
and accordingly. Both machines for deploy purposes should have the
**config.load_balancing.is_master** set to **true** and The
**config.load_balancing.master.slave_postgres_ssh_keys** and
**config.load_balancing.master.slave_agoraelections_ssh_keys** set to **[]**
(which means empty list) at this stage of deployment.

After setting the configuration, you should set the playbook that we will use
for deploying as master the machines, and also copy the ansible inventory used to
specify that the deployment is done locally, then execute ansible with both of
them:

    agora@agora:~/agora-dev-box/ $ cp doc/production/playbook.agora.yml playbook.yml
    agora@agora:~/agora-dev-box/ $ cp doc/production/local.inventory inventory
    agora@agora:~/agora-dev-box/ $ time sudo ansible-playbook -i inventory playbook.yml

Once this is done, the initial as-master deployment has been successful.

If you have assigned a FQDN to for example 'agora.example.com' to the machine
and the name resolution is set up correctly in your personal machine via DNS or
by adding 'agora.example.com ipaddr' to your '/etc/hosts', you should be able to login
as an administrator entering in 'https://agora.example.com/admin/login' using
the credentials you specified in the config.yml file.

We recommend to use the /etc/hosts file to change the ip address of the
webserver from agora1 to agora2 ip easily for testing purposes.

# Deployment of authorities [auth1, auth2]

The following steps should be executed in both election authorities. Download
the deployment script:

    agora@auth:~ $ git clone https://github.com/agoravoting/agora-dev-box.git
    agora@auth:~ $ cd agora-dev-box
    agora@auth:~/agora-dev-box/ $ git checkout feature_load_balancing_high_availability

We'll use an authority config file as a base:

    agora@auth:~/agora-dev-box/ $ cp doc/production/config.auth.yml config.yml

Edit the config.yml file following the instructions inside, then copy the
appropiate inventory and playbook, then launch the ansible deployment script:

    agora@auth:~/agora-dev-box/ $ cp doc/production/playbook.auth.yml playbook.yml
    agora@auth:~/agora-dev-box/ $ cp doc/production/local.inventory inventory
    agora@auth:~/agora-dev-box/ $ time sudo ansible-playbook -i inventory playbook.yml

### Connecting auth1 with auth2

Authorities communicate with other authorities using ssl and client
certificates so the authority server doesn't accept queries from unknown
servers. In a real election system it's a good idea to not publish the ips
and ports of the authorities to avoid malicious attacks.

The deployment script creates a certificate for each authority in
/srv/cert/selfsigned/ and we manage the authority communication and
certificate sharing with the eopeers tool.

Execute the following in **auth1**:

    agora@auth1:~ $ sudo eopeers --show-mine

Copy the output to a file in **auth2**, then install it:

    agora@auth2:~ $ sudo sudo eopeers --install auth1.pkg
    agora@auth2:~ $ sudo service nginx restart

Then do the same the other way around:

    agora@auth2:~ $ sudo eopeers --show-mine

    agora@auth1:~ $ sudo sudo eopeers --install auth2.pkg
    agora@auth1:~ $ sudo service nginx restart

### Test the connection between the authorities

A tool is installed to test the real connection between the authorities.
Open two terminal windows.  Open eolog in one of the terminal windows:

    agora@auth2 $ sudo eolog

Run eotest in the other terminal window from the other auth server:

    agora@auth1 $ sudo eotest full --vmnd --vcount 100

You should see the software working as eolog output will appear in the
first terminal window. Once it the eotest command finishes, you can also close
auth2 connection to eolog.

### Connecting agora servers with authorities

The following commands should be executed in both **agora1** and **agora2**
machines:

Create **auth1.pkg** and **auth2.pkg** files with the configuration of both
authorities. Then install them in the agora server:

    agora@agora:~ $ sudo eopeers --install auth1.pkg --keystore /home/agoraelections/keystore.jks
    agora@agora:~ $ sudo eopeers --install auth2.pkg
    agora@agora:~ $ sudo service nginx restart

Before completion, the installation of the agora certificate should be installed
in the

    $ cd agora
    agora $ scp -F vagrant.ssh.config ../auth1/auth1.pkg ../auth2/auth2.pkg default:/home/vagrant/
    agora $ vagrant ssh -c "sudo eopeers --install /home/vagrant/auth1.pkg --keystore /home/agoraelections/keystore.jks; sudo eopeers --install /home/vagrant/auth2.pkg; sudo service nginx restart"
    agora $ cd ..
