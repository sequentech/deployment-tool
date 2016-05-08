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

    root@agora # adduser agora agora --gecos "FullName,RoomNumber,WorkPhone,HomePhone" --disabled-password

Afterwards, you should add the permissions that the agora user requires for
administration and deployment.

This is how you do it in the two servers that will be used as authorities:

    root@agora # wget https://raw.githubusercontent.com/agoravoting/agora-dev-box/next/doc/production/auth.sudoers
    root@agora # cat auth.sudoers >> /etc/sudoers

And this is how you do it for the two other servers that will be used as master
and slave machines:

    root@agora # wget https://raw.githubusercontent.com/agoravoting/agora-dev-box/next/doc/production/agora.sudoers
    root@agora # cat agora.sudoers >> /etc/sudoers


- Install initial dependencies

Once permissions have been granted, we'll continue to execute everything through
the **agora** user. Now We need to install some requirements needed to continue:

    agora@agora:~ $ sudo apt-get install software-properties-common pwgen -y
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
-  auth1 <<tcp:4081>> auth2 # vfork
-  auth1 <<udp:8081>> auth2 # vfork

# Agora web servers master deployment [agora1, agora2]

The following steps should be executed in both web servers. Download the
deployment script:

    agora@agora:~ $ git clone https://github.com/agoravoting/agora-dev-box.git
    agora@agora:~ $ cd agora-dev-box
    agora@agora:~/agora-dev-box/ $ git checkout next

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

If your machine is behind a proxy, you need to specify that in the
**config.has_https_proxy** variable.

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

# Configure agora2 as a slave

To configure agora2 as a slave, we need to import the ssh keys from the
agoraelections and postgres users in ***agora1*** to add them in ***agora2**.

To get the keys execute these commands in ***agora2***:

    agora@agora2:~/agora-dev-box/ $ sudo -u agoraelections cat /home/agoraelections/.ssh/id_rsa.pub
    agora@agora2:~/agora-dev-box/ $ sudo -u postgres cat /var/lib/postgresql/.ssh/id_rsa.pub

Copy those keys and set them in the **agora1** **config.yml** file in
the variables **config.load_balancing.master.slave_agoraelections_ssh_keys**
and **config.load_balancing.master.slave_postgres_ssh_keys**.

Then, execute again ansible in ***agora1*** to apply the changes:

    agora@agora1:~/agora-dev-box/ $ time sudo ansible-playbook -i inventory playbook.yml -v

After that, then you can change the **config.yml** for **agora2** to set
the variable **config.load_balancing.is_master** to **false** and
**config.load_balancing.slave.master_hostname** to the hostname of **agora1**.

If your machine is behind a proxy, you need to specify that in the
**config.has_https_proxy** variable.

Then you can run again ansible in **agora2** to apply the changes, using the
slave specific playbook, which can only work after having executed
**playbook.agora.yml**:

    agora@agora2:~/agora-dev-box/ $ cp doc/production/playbook.slave.yml playbook.yml
    agora@agora2:~/agora-dev-box/ $ time sudo ansible-playbook -i inventory playbook.yml

# Deployment of authorities [auth1, auth2]

The following steps should be executed in both election authorities. Download
the deployment script:

    agora@auth:~ $ git clone https://github.com/agoravoting/agora-dev-box.git
    agora@auth:~ $ cd agora-dev-box
    agora@auth:~/agora-dev-box/ $ git checkout next

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
authorities. Then install them:

    agora@agora:~ $ sudo eopeers --install auth1.pkg --keystore /home/agoraelections/keystore.jks
    agora@agora:~ $ sudo eopeers --install auth2.pkg
    agora@agora:~ $ sudo service nginx restart

Before completion, the installation of the certificate of the **agora1** and
**agora2** servers needs to be installed in the election authorities, because
even though i'ts the same TLS cert, they have different hostnames. So copy
them (get it with "eopeers --show-mine") to the authorities and install them:

    agora@agora:~ $ sudo eopeers --install agora1.pkg
    agora@agora:~ $ sudo eopeers --install agora2.pkg
    agora@agora:~ $ sudo service nginx restart

### Create a test election

Go to https://agora1/admin/login and create a test election. Then execute
the following to create some votes. Change '2' in the following commands with
your election number:

    agora@agora1:~ $ su - agoraelections
    agoraelections@agora1:~ $ source ~/env/bin/activate
    agoraelections@agora1:~ $ cd ~/agora-elections/admin
    agoraelections@agora1:~ $ export ELECTION_ID=2
    agoraelections@agora1:~/agora-elections/admin/ $ ./admin.py dump_pks $ELECTION_ID
    agoraelections@agora1:~/agora-elections/admin/ $ echo '[1,0]' > votes.json
    agoraelections@agora1:~/agora-elections/admin/ $ ./admin.py encrypt $ELECTION_ID

start the election, cast the votes, stop it and tally it:

    agoraelections@agora1:~/agora-elections/admin/ $ ./admin.py start $ELECTION_ID
    agoraelections@agora1:~/agora-elections/admin/ $ ./admin.py cast_votes $ELECTION_ID
    agoraelections@agora1:~/agora-elections/admin/ $ ./admin.py count_votes $ELECTION_ID
    2 (2)
    agoraelections@agora1:~/agora-elections/admin/ $ ./admin.py stop $ELECTION_ID
    agoraelections@agora1:~/agora-elections/admin/ $ ./admin.py tally $ELECTION_ID

### Check high availability and load balancing

The high availability configuration in this configuration basically means that
**agora2** is a server that is replicating in a hot standby mode the database of
**agora1**. **agora2** has also replicated everything needed to be able to
change the server from slave to master at any time.

To test that **agora2** is correctly deployed as a slave, you can directly
connect to https://agora2/admin/login and it should allow you to access and work
normally, because **agora2** is a slave that also works as a web server
(authapi, agora-elections) connected directly to the **agora1** master database
server.

If you list the files inside the datastore and the server certificate in
both **agora1** and **agora2**, it should list the same files:

    agora@agora:~ $ sudo -u agoraelections find /home/agoraelections/datastore/ -type f | xargs md5sum
    05b76ec89dd7a32b76427d389a5778c1  /home/agoraelections/datastore/public/2/pks

    agora@agora:~ $ find /srv/certs/selfsigned/ -type f | xargs md5sum
    d811c3e92162ade25f21f1d782f32c6e  /srv/certs/selfsigned/calist
    54a67dfe2a9fde364a833135d9bfdd3b  /srv/certs/selfsigned/key-nopass.pem
    a9bf327511b67100c096aebed5b46c94  /srv/certs/selfsigned/cert.pem

### Test changing a slave to be a master and do a tally

This requires to create an election in **agora1** and cast some votes, then
launch the tally successfully from within the authorities.

To promote **agora2** to be a master, change set to **true** the config.yml
config variable **config.load_balancing.is_master**, then execute again ansible:

    agora@agora2:~/agora-dev-box/ $ time sudo ansible-playbook -i inventory playbook.yml

To be able to receive successfully the tally, agora2 needs to "impersonate"
agora1 in the director election authority. This can be done by:

1. removing the agora1 eopeer package:

    agora@auth1:~ $ sudo eopeers --remove agora1

2. adding an alias to /etc/hosts in **auth1** config.yml variable **config.hosts**,
   setting it to something like:

    hosts:
    - hostname: agora1
      ip: 192.168.50.14

3. re-executing ansible in **auth1**:

    agora@auth1:~/agora-dev-box/ $ time sudo ansible-playbook -i inventory playbook.yml

### Troubleshooting

For Troubleshooting please read the deployment_troubleshooting.md file.
