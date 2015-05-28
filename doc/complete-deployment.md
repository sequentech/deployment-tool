# Complete Agora Voting deployment system

This document describes the complete deployment of an Agora Voting system
with two Authorities.

## agora-dev-box

First of all we need to download the ansible deployment project:

    $ git clone https://github.com/agoravoting/agora-dev-box.git

Note: sometimes the 'next' branch has important updates. In case you want
to use the 'next' branch, do:

    $ git checkout next

## Servers

We need at least 3 servers to deploy a secure environment. We'll have two
authorities and then other server with the authentication (authapi), the
web interface (agora-core-view) and the ballot box (aogra\_elections).

The deployment is tested with ubuntu/trusty64, it should work with other
ubuntu distributions, but maybe the deployment needs some tweaks.

## Vagrant machines

If you have real machines you can skip this step, but be sure to modify
each config file to use your currently real ips.

First of all we'll create the three servers we need with vagrant, copy the
agora-dev-box folder three times with different names, one for each server:

    $ cp -r agora-dev-box auth1
    $ cp -r agora-dev-box auth2
    $ cp -r agora-dev-box agora

Then we can create each Vagrant machine. Note: if we want to assign more memory or number of cpu to
vagrant machine for a faster installation, we can edit Vagrantfile and change v.memory (memory in
MB) and v.cpus (number of cpu):

    $ cd auth1
    auth1 $ cp doc/Vagrantfile.auth1 Vagrantfile
    auth1 $ vagrant up --no-provision
    auth1 $ vagrant ssh-config > ./vagrant.ssh.config

    $ cd auth2
    auth2 $ cp doc/Vagrantfile.auth2 Vagrantfile
    auth2 $ vagrant up --no-provision
    auth2 $ vagrant ssh-config > ./vagrant.ssh.config

    $ cd agora
    agora $ cp doc/Vagrantfile.agora Vagrantfile
    agora $ vagrant up --no-provision
    agora $ vagrant ssh-config > ./vagrant.ssh.config

Now we've three basic ubuntu machines connected with this ips:

 * auth1: 192.168.50.2
 * auth2: 192.168.50.3
 * agora: 192.168.50.4

So you should add this to your /etc/hosts to be able to access:

    echo "192.168.50.2 local-auth1" >> /etc/hosts
    echo "192.168.50.3 local-auth2" >> /etc/hosts
    echo "192.168.50.4 agora" >> /etc/hosts

## Authorities server

We need to deploy the two authorities and connect them. The process is the
same for deploy this two authorities.

    $ cd auth1
    auth1 $ cp doc/auth1.config.yml config.yml
    auth1 $ cp doc/auth.playbook.yml playbook.yml
    auth1 $ vagrant provision
    auth1 $ vagrant ssh
    local-auth1 $ sudo eopeers --show-mine | tee /home/vagrant/auth1.pkg >/dev/null
    local-auth1 $ exit
    auth1 $ scp -F vagrant.ssh.config default:/home/vagrant/auth1.pkg auth1.pkg

    $ cd auth2
    auth2 $ cp doc/auth2.config.yml config.yml
    auth2 $ cp doc/auth.playbook.yml playbook.yml
    auth2 $ vagrant provision
    auth2 $ vagrant ssh
    local-auth2 $ sudo eopeers --show-mine | tee /home/vagrant/auth2.pkg >/dev/null
    local-auth2 $ exit
    auth2 $ scp -F vagrant.ssh.config default:/home/vagrant/auth2.pkg auth2.pkg

Then we've these two servers running with all authority software installed
and running.

### Reconfiguring locales

This step is only needed if you found an error on the previous step when executing 'vagrant provision'. If when you executed 'vagrant provision' you got this kind of error:

    TASK: [Election orchestra, Create Database User] ****************************** 
    failed: [default] => {"failed": true}
    msg: unable to connect to database: could not connect to server: No such file or directory
            Is the server running locally and accepting
            connections on Unix domain socket "/var/run/postgresql/.s.PGSQL.5432"?
            
Then you should reconfigure the locales configuration:

    vagrant ssh
    sudo su
    locale

That command will show you all the locales you need to install, then you will need to do something similar to:

    locale-gen en_US en_US.UTF-8 es_ES es_ES.UTF-8
    dpkg-reconfigure locales
    psql --version
    pg_createcluster 9.3 main
    /etc/init.d/postgresql start
    exit
    exit

Now you should be able to execute 'vagrant provision' without errors. A cleaner option is to do the locale-gen and dpkg-reconfigure just after the 'vagrant up --no-provision' command, avoiding getting an error before the first vagrant provision.

### Connecting auth1 with auth2

Authorities talks to other authorities using ssl and client certificate so
the authority server doesn't accept querires from not known servers. In a
real election system it's a good idea to not publish authorities ips and
ports to avoid malicious attacks.

The deployment script creates a certificate for each authority in
/srv/cert/serlfsigned/ and we manage the authority communication and
certificate sharing with eopeers tool.

    $ cd auth1
    auth1 $ scp -F vagrant.ssh.config ../auth2/auth2.pkg default:/home/vagrant/auth2.pkg
    auth1 $ vagrant ssh
    auth1 $ sudo eopeers --install /home/vagrant/auth2.pkg
    auth1 $ sudo service nginx restart

    $ cd auth2
    auth2 $ scp -F vagrant.ssh.config ../auth1/auth1.pkg default:/home/vagrant/auth1.pkg
    auth2 $ vagrant ssh
    auth2 $ sudo eopeers --install /home/vagrant/auth1.pkg
    auth2 $ sudo service nginx restart

### Test the authorities connection

To test the authorities real connection there's a tool installed, so after
the certificate installation you can run the test command:

    $ cd auth1
    auth1 $ vagrant ssh
    local-auth1 $ sudo eotest full --vmnd --vcount 100

To view the software working in the other authority you can use the eolog
in other terminal.

    $ cd auth2
    auth2 $ vagrant ssh
    local-auth2 $ sudo eolog

## Agora server (part 1)

    $ cd agora
    agora $ cp doc/agora.config.yml config.yml
    agora $ cp doc/agora.playbook.yml playbook.yml
    agora $ vagrant provision

    agora $ vagrant ssh
    agora $ sudo eopeers --show-mine | tee /home/vagrant/agora.pkg >/dev/null
    agora $ exit

    agora $ scp -F vagrant.ssh.config default:/home/vagrant/agora.pkg agora.pkg

### Connecting agora server with authorities

The ballotbox should be able to communicate with the authorities. We'll
user local-auth1 as the director authority, but we need to add all
authorities to our eopeers.

    $ cd auth1
    auth1 $ scp -F vagrant.ssh.config ../agora/agora.pkg default:/home/vagrant/agora.pkg
    auth1 $ vagrant ssh
    local-auth1 $ sudo eopeers --install /home/vagrant/agora.pkg
    local-auth1 $ sudo service nginx restart
    local-auth1 $ exit

    $ cd auth2
    auth2 $ scp -F vagrant.ssh.config ../agora/agora.pkg default:/home/vagrant/agora.pkg
    auth2 $ vagrant ssh
    local-auth2 $ sudo eopeers --install /home/vagrant/agora.pkg
    local-auth2 $ sudo service nginx restart
    local-auth2 $ exit

    $ cd agora
    agora $ scp -F vagrant.ssh.config ../auth1/auth1.pkg default:/home/vagrant/auth1.pkg
    agora $ scp -F vagrant.ssh.config ../auth2/auth2.pkg default:/home/vagrant/auth2.pkg
    agora $ vagrant ssh
    agora $ sudo eopeers --install /home/vagrant/auth1.pkg --keystore /home/agoraelections/keystore.jks
    agora $ sudo eopeers --install /home/vagrant/auth2.pkg
    agora $ sudo service nginx restart
    agora $ exit


## Agora server (part 2)

    cd agora
    agora $ vagrant ssh
    agora $ sudo supervisorctl stop agora-elections
    agora $ sudo su - agoraelections
    agora $ cd /home/agoraelections/agora-elections
    agora $ ../activator-1.2.12-minimal/activator run

Then you should go to the following url in your local browser:

    http://agora:9000/elections/api/election/1

It should return a 404, but that will also create the agora\_elections database
and we can continue configuring this server.

    agora $ ../activator-1.2.12-minimal/activator clean stage
    agora $ exit
    agora $ sudo supervisorctl start agora-elections
    agora $ exit

There we go, so currently we've a complete agora-voting installation and
this should work.

### Complete election test with agora-tools

Currently there's no a election creation form, but you can create an
election using agora-admin.py in agora-tools

Download agora-tools and make it work:

    $ git clone https://github.com/agoravoting/agora-tools.git
    $ cd agora-tools

Note: sometimes the 'next' branch has important updates. In case you want
to use the 'next' branch, do:

    $ git checkout next
    
Make it work:

    agora-tools $ mkvirtualenv -p $(which python3) agora-tools
    agora-tools $ pip install -r requirements.txt
    agora-tools $ cp -r ../agora-dev-box/doc/agora-tools-configs/ localconfs

Then you can edit the local election data, be sure to change at least the
census file localconfs/data/local/0.census.json and add real emails.

    agora-tools $ ./agora-admin.py -C localconfs/local.email.json -c localconfs/data/local/

This should create the election and will give you the election id. The
first time the election id should be 1.

Now we need to configure authapi, open the browser and enter this webpage:

    http://agora/authapi/admin/

Use the default credentials (or the ones you set on local.email.json):

    username: admin
    password: 123
    
Once you are here, you need to fix the event for the admin to 1. Click on 'User datas' below 'Api' and select admin. If you see that the selected Event is '--------'  you need to click on the drop'down list and select '1 - open' instead and then click Save.

Go back to the main authapi configuration page and click on 'Codes' under 'Authmethods', then click on 'add code'. On the Add code page, use the following and then click Save (you can change the code):

    User: admin
    Code: qwerty33
    Auth event id: 1

Then you can open your broswer and make the rest of the election using the
admin:

    http://agora/#/admin/login

Use the default credentials:

    email: admin@agoravoting.com
    password: qwerty33

Then you should view the list of elections you have. You can go to the
dashboard clicking on the green engine in the list.

From the dashboard you can start the voting, send the auth codes (once the
election is started you can click in the paper plane button, look in your
spam folder), stop the election, make the tally and view the results.

The admin interface is currently in development so there're a lot of buttons
that might not work.
