# Complete Agora Voting deployment system

This document describes the complete deployment of an Agora Voting system
with two Authorities.

## agora-dev-box

First of all we need to download the ansible deployment project:

    $ git clone https://github.com/agoravoting/agora-dev-box.git

Note: sometimes the 'next' branch has important updates. In case you want
to use the 'next' branch, do:

    $ cd agora-dev-box
    $ git checkout next
    $ cd ..

## Servers

We need at least 3 servers to deploy a secure environment. We'll have two
authorities and then another server with the authentication (authapi), the
web interface (agora-gui) and the ballot box (aogra\_elections).

The deployment is tested with ubuntu/trusty64, it should work with other
ubuntu distributions, but maybe the deployment needs some tweaks.

## Vagrant machines

If you have real machines you can skip this step, but be sure to modify
each config file to use your real ips.

First of all we'll create the three servers we need with vagrant. Copy the
agora-dev-box folder three times with different names, one for each server:

    $ cp -r agora-dev-box auth1
    $ cp -r agora-dev-box auth2
    $ cp -r agora-dev-box agora

Then we can create each Vagrant machine. Note: if we want to assign more
memory or a different number of cpus to the vagrant machines for a faster
installation, we can edit Vagrantfile and change v.memory (memory in MB)
and v.cpus (number of cpus):

    $ cd auth1
    auth1 $ cp doc/Vagrantfile.auth1 Vagrantfile
    auth1 $ vagrant up --no-provision
    auth1 $ vagrant ssh-config > ./vagrant.ssh.config
    auth1 $ cd ..

    $ cd auth2
    auth2 $ cp doc/Vagrantfile.auth2 Vagrantfile
    auth2 $ vagrant up --no-provision
    auth2 $ vagrant ssh-config > ./vagrant.ssh.config
    auth2 $ cd ..

    $ cd agora
    agora $ cp doc/Vagrantfile.agora Vagrantfile
    agora $ vagrant up --no-provision
    agora $ vagrant ssh-config > ./vagrant.ssh.config
    agora $ cd ..

Now we've three basic Ubuntu 14.04.3 LTS (Trusty Tahr) machines connected with these ips:

 * auth1: 192.168.50.2
 * auth2: 192.168.50.3
 * agora: 192.168.50.4

So you should add this to your /etc/hosts to be able to access them by name:

    echo "192.168.50.2 local-auth1" >> /etc/hosts
    echo "192.168.50.3 local-auth2" >> /etc/hosts
    echo "192.168.50.4 agora" >> /etc/hosts

If you receive the message `/etc/hosts: Permission denied` try:

    echo "192.168.50.2 local-auth1" | sudo tee -a /etc/hosts
    echo "192.168.50.3 local-auth2" | sudo tee -a /etc/hosts
    echo "192.168.50.4 agora" | sudo tee -a /etc/hosts

## Authorities server

We need to deploy the two authorities and connect them. The deployment
process is the same for both authorities.

    $ cd auth1
    auth1 $ cp doc/auth1.config.yml config.yml
    auth1 $ cp doc/auth.playbook.yml playbook.yml
    auth1 $ vagrant provision
    auth1 $ vagrant ssh
    local-auth1 $ sudo eopeers --show-mine | tee /home/vagrant/auth1.pkg >/dev/null
    local-auth1 $ exit
    auth1 $ scp -F vagrant.ssh.config default:/home/vagrant/auth1.pkg auth1.pkg
    auth1 $ cd ..

    $ cd auth2
    auth2 $ cp doc/auth2.config.yml config.yml
    auth2 $ cp doc/auth.playbook.yml playbook.yml
    auth2 $ vagrant provision
    auth2 $ vagrant ssh
    local-auth2 $ sudo eopeers --show-mine | tee /home/vagrant/auth2.pkg >/dev/null
    local-auth2 $ exit
    auth2 $ scp -F vagrant.ssh.config default:/home/vagrant/auth2.pkg auth2.pkg
    auth2 $ cd ..

Now we have these two servers running with all authority software installed
and running.

### Reconfiguring locales

This step is only needed if you found an error on the previous step when
executing 'vagrant provision'. If when you executed 'vagrant provision' you
got this kind of error:

    TASK: [Election orchestra, Create Database User] ******************************
    failed: [default] => {"failed": true}
    msg: unable to connect to database: could not connect to server: No such file or directory
            Is the server running locally and accepting
            connections on Unix domain socket "/var/run/postgresql/.s.PGSQL.5432"?

Then you should reconfigure the locales configuration:

    vagrant ssh
    sudo su
    locale

That command will show you all the locales you need to install, then you
will need to do something similar to:

    locale-gen en_US en_US.UTF-8 es_ES es_ES.UTF-8
    dpkg-reconfigure locales
    psql --version
    pg_createcluster 9.3 main
    /etc/init.d/postgresql start
    exit
    exit

Now you should be able to execute 'vagrant provision' without errors. A
cleaner option is to do the locale-gen and dpkg-reconfigure just after the
'vagrant up --no-provision' command, avoiding getting an error before the
first vagrant provision.

### Connecting auth1 with auth2

Authorities communicate with other authorities using ssl and client
certificates so the authority server doesn't accept queries from unknown
servers. In a real election system it's a good idea to not publish the ips
and ports of the authorities to avoid malicious attacks.

The deployment script creates a certificate for each authority in
/srv/cert/selfsigned/ and we manage the authority communication and
certificate sharing with the eopeers tool.

    $ cd auth1
    auth1 $ scp -F vagrant.ssh.config ../auth2/auth2.pkg default:/home/vagrant/auth2.pkg
    auth1 $ vagrant ssh
    local-auth1 $ sudo eopeers --install /home/vagrant/auth2.pkg
    local-auth1 $ sudo service nginx restart
    local-auth1 $ exit
    auth1 $ cd ..

    $ cd auth2
    auth2 $ scp -F vagrant.ssh.config ../auth1/auth1.pkg default:/home/vagrant/auth1.pkg
    auth2 $ vagrant ssh
    local-auth2 $ sudo eopeers --install /home/vagrant/auth1.pkg
    local-auth2 $ sudo service nginx restart
    local-auth2 $ exit
    auth2 $ cd ..

### Test the connection between the authorities

A tool is installed to test the real connection between the authorities.
Open two terminal windows.  Open eolog in one of the terminal windows:

    $ cd auth2
    auth2 $ vagrant ssh
    local-auth2 $ sudo eolog

Run eotest in the other terminal window from the other auth server:

    $ cd auth1
    auth1 $ vagrant ssh
    local-auth1 $ sudo eotest full --vmnd --vcount 100

You should see the software working as eolog output will appear in the
first terminal window.

Close the second terminal window.
Exit the auth2 server:

    local-auth2 $ exit
    auth2 $ cd ..

## Agora server (part 1)

    $ cd agora
    agora $ cp doc/agora.config.yml config.yml
    agora $ cp doc/agora.playbook.yml playbook.yml
    agora $ vagrant provision

    agora $ vagrant ssh
    local-agora $ sudo eopeers --show-mine | tee /home/vagrant/agora.pkg >/dev/null
    local-agora $ exit

    agora $ scp -F vagrant.ssh.config default:/home/vagrant/agora.pkg agora.pkg
    agora $ cd ..

### Connecting agora server with authorities

The ballotbox should be able to communicate with the authorities. We'll
use local-auth1 as the director authority, but we need to add all
authorities to our eopeers.

    $ cd auth1
    auth1 $ scp -F vagrant.ssh.config ../agora/agora.pkg default:/home/vagrant/agora.pkg
    auth1 $ vagrant ssh
    local-auth1 $ sudo eopeers --install /home/vagrant/agora.pkg
    local-auth1 $ sudo service nginx restart
    local-auth1 $ exit
    auth1 $ cd ..

    $ cd auth2
    auth2 $ scp -F vagrant.ssh.config ../agora/agora.pkg default:/home/vagrant/agora.pkg
    auth2 $ vagrant ssh
    local-auth2 $ sudo eopeers --install /home/vagrant/agora.pkg
    local-auth2 $ sudo service nginx restart
    local-auth2 $ exit
    auth2 $ cd ..

    $ cd agora
    agora $ scp -F vagrant.ssh.config ../auth1/auth1.pkg default:/home/vagrant/auth1.pkg
    agora $ scp -F vagrant.ssh.config ../auth2/auth2.pkg default:/home/vagrant/auth2.pkg
    agora $ vagrant ssh
    local-agora $ sudo eopeers --install /home/vagrant/auth1.pkg --keystore /home/agoraelections/keystore.jks
    local-agora $ sudo eopeers --install /home/vagrant/auth2.pkg
    local-agora $ sudo service nginx restart
    local-agora $ exit
    agora $ cd ..

Having completed these steps, we now have a complete agora-voting installation.

### Complete election test with agora-tools

Currently there's no election creation form, but you can create an
election using agora-admin.py in agora-tools.

Download and configure agora-tools:

    $ git clone https://github.com/agoravoting/agora-tools.git
    $ cd agora-tools

Note: sometimes the 'next' branch has important updates. In case you want
to use the 'next' branch, do:

    $ git checkout next

You must have Python 3 installed to complete the following steps.

Install dependencies:

    agora-tools $ mkvirtualenv -p $(which python3) agora-tools
    agora-tools $ pip install -r requirements.txt
    agora-tools $ cp -r ../agora-dev-box/doc/agora-tools-configs/ localconfs

Then you can edit the local election data, be sure to change at least the
census file localconfs/data/local/0.census.json and add real emails.

    agora-tools $ ./agora-admin.py -C localconfs/local.email.json -c localconfs/data/local/

This should create the election and will give you the election id. The
first time the election id should be 1.

Now we need to configure authapi. Open the browser and enter this url:

    https://agora/authapi/admin/

Use the default credentials (or the ones you set in local.email.json):

    username: admin
    password: 123

Once you are here, you need to fix the event for the admin to 1. Click on
'User datas' below 'Api' and select admin. If you see that the selected
Event is '--------'  you need to click on the drop'down list and select
'1 - open' instead and then click Save.

Go back to the main authapi configuration page and click on 'Codes' under
'Authmethods', then click on 'add code'. On the Add code page, use the
following and then click Save (you can change the code):

    User: admin
    Code: QWERTY33
    Auth event id: 1

Then you can open your broswer and make the rest of the election using the
admin:

    https://agora/#/admin/login

Use the default credentials:

    Email: admin@agoravoting.com
    Authentication Code: QWERTY33

Then you should view the list of elections you have. You can go to the
dashboard clicking on the green engine in the list.

From the dashboard you can start the voting, send the auth codes (once the
election is started you can click in the paper plane button, look in your
spam folder), stop the election, make the tally and view the results.

The admin interface is currently in development so there're a lot of buttons
that might not work.
