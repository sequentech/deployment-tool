# Complete Agora Voting deployment system

This document describes the complete deployment of an Agora Voting system
with two Authorities for development purpuoses in your own physical machine
through the usage of virtual machines. We call it a development environment.

## Requirements

You need a Linux x64 host machine with at least 4GB of RAM.

- Vagrant

We will use vagrant for managing the virtual machines. We recomend you to use
the [latest version of vagrant that can be downloaded from here](https://www.vagrantup.com/downloads.html).

- Vagrant snasphots plugin

We'll use a vagrant plugin to create snapshots of the virtual machines.
Snapshots allow us to go back and forth to a specific states of the virtual
machines.

You can install this plugin after having installed vagrant with the following
command that needs to be executed with the user that will execute vagrant (not
root):

    vagrant plugin install vagrant-vbox-snapshot

- VirtualBox

To provision the virtual machines we'll make use of VirtualBox. Again, we
recommend you to use the [latest version of VirtualBox that can be downloaded from here](https://www.virtualbox.org/wiki/Linux_Downloads).

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
    auth1 $ cp doc/devel/Vagrantfile.auth1 Vagrantfile
    auth1 $ vagrant up --no-provision && vagrant ssh-config > ./vagrant.ssh.config && vagrant snapshot take zero
    auth1 $ cd ..

    $ cd auth2
    auth2 $ cp doc/devel/Vagrantfile.auth2 Vagrantfile
    auth2 $ vagrant up --no-provision && vagrant ssh-config > ./vagrant.ssh.config && vagrant snapshot take zero
    auth2 $ cd ..

    $ cd agora
    agora $ cp doc/devel/Vagrantfile.agora Vagrantfile
    agora $ vagrant up --no-provision && vagrant ssh-config > ./vagrant.ssh.config && vagrant snapshot take zero
    agora $ cd ..

Now we've three basic Ubuntu 14.04.3 LTS (Trusty Tahr) machines connected with these ips:

 * auth1: 192.168.50.2
 * auth2: 192.168.50.3
 * agora: 192.168.50.4

So you should add this to your local machine /etc/hosts to be able to access them by name:

    echo -e "192.168.50.2 local-auth1\n192.168.50.3 local-auth2\n192.168.50.4 agora"  | sudo tee -a /etc/hosts

## Base provisioning

Although recommended, this step can be ignored. This step will allow us to
create a basic VM snapshot with java and other package dependencies installed
so that provisioning can be done in a quicker manner.

    $ cd auth1
    auth1 $ cp doc/devel/auth1.config.yml config.yml
    auth1 $ cp doc/devel/base.playbook.yml playbook.yml
    auth1 $ vagrant provision
    auth1 $ vagrant snapshot take base

    $ cd auth2
    auth2 $ cp doc/devel/auth2.config.yml config.yml
    auth2 $ cp doc/devel/base.playbook.yml playbook.yml
    auth2 $ vagrant provision
    auth2 $ vagrant snapshot take base

    $ cd agora
    agora $ cp doc/devel/agora.config.yml config.yml
    agora $ cp doc/devel/base.playbook.yml playbook.yml
    agora $ vagrant provision
    agora $ vagrant snapshot take base

## Authorities server

### Provisioning

We need to deploy the two authorities and connect them. The deployment
process is the same for both authorities.

    $ cd auth1
    auth1 $ cp doc/devel/auth1.config.yml config.yml
    auth1 $ cp doc/devel/auth.playbook.yml playbook.yml
    auth1 $ vagrant provision
    auth1 $ vagrant ssh -c "sudo eopeers --show-mine | tee /home/vagrant/auth1.pkg >/dev/null"
    auth1 $ scp -F vagrant.ssh.config default:/home/vagrant/auth1.pkg auth1.pkg
    auth1 $ cd ..

    $ cd auth2
    auth2 $ cp doc/devel/auth2.config.yml config.yml
    auth2 $ cp doc/devel/auth.playbook.yml playbook.yml
    auth2 $ vagrant provision
    auth2 $ vagrant ssh -c "sudo eopeers --show-mine | tee /home/vagrant/auth2.pkg >/dev/null"
    auth2 $ scp -F vagrant.ssh.config default:/home/vagrant/auth2.pkg auth2.pkg
    auth2 $ cd ..

Now we have these two servers running with all authority software installed
and running.

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
    auth1 $ vagrant ssh -c "sudo eopeers --install /home/vagrant/auth2.pkg && sudo service nginx restart"
    auth1 $ cd ..

    $ cd auth2
    auth2 $ scp -F vagrant.ssh.config ../auth1/auth1.pkg default:/home/vagrant/auth1.pkg
    auth1 $ vagrant ssh -c "sudo eopeers --install /home/vagrant/auth1.pkg && sudo service nginx restart"
    auth2 $ cd ..

### Test the connection between the authorities

A tool is installed to test the real connection between the authorities.
Open two terminal windows.  Open eolog in one of the terminal windows:

    $ cd auth2
    auth2 $ vagrant ssh -c "sudo eolog"

Run eotest in the other terminal window from the other auth server:

    $ cd auth1
    auth1 $ vagrant ssh -c "sudo eotest full --vmnd --vcount 100"

You should see the software working as eolog output will appear in the
first terminal window. Once it the eotest command finishes, you can also close
auth2 connection to eolog.

### Save snapshots

Once you have completed a complete test of the authorities and they are in
working condition, it's recommended to save a snapshot from both:

    $ cd auth1
    auth1 $ vagrant snapshot take eotest-worked
    auth1 $ cd ..

    $ cd auth2
    auth2 $ vagrant snapshot take eotest-worked
    auth2 $ cd ..

## Agora server (part 1)

Let's provision the agora server in a similar fashion as we did with the
authorities:

    $ cd agora
    agora $ cp doc/devel/agora.config.yml config.yml
    agora $ cp doc/devel/agora.playbook.yml playbook.yml
    agora $ vagrant provision
    agora $ vagrant ssh -c "sudo eopeers --show-mine | tee /home/vagrant/agora.pkg >/dev/null"
    agora $ scp -F vagrant.ssh.config default:/home/vagrant/agora.pkg agora.pkg
    agora $ cd ..

### Connecting agora server with authorities

The ballotbox should be able to communicate with the authorities. We'll
use local-auth1 as the director authority, but we need to add all
authorities to our eopeers.

    $ cd auth1
    auth1 $ scp -F vagrant.ssh.config ../agora/agora.pkg default:/home/vagrant/agora.pkg
    auth1 $ vagrant ssh -c "sudo eopeers --install /home/vagrant/agora.pkg; sudo service nginx restart"
    auth1 $ cd ..

    $ cd auth2
    auth2 $ scp -F vagrant.ssh.config ../agora/agora.pkg default:/home/vagrant/agora.pkg
    auth2 $ vagrant ssh -c "sudo eopeers --install /home/vagrant/agora.pkg; sudo service nginx restart"
    auth2 $ cd ..

    $ cd agora
    agora $ scp -F vagrant.ssh.config ../auth1/auth1.pkg ../auth2/auth2.pkg default:/home/vagrant/
    agora $ vagrant ssh -c "sudo eopeers --install /home/vagrant/auth1.pkg --keystore /home/agoraelections/keystore.jks; sudo eopeers --install /home/vagrant/auth2.pkg; sudo service nginx restart"
    agora $ cd ..

Having completed these steps, we now have a complete agora-voting installation.

### Complete election test

You can open your broswer and make the rest of the election using the admin:

    https://agora/admin/login

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

Once you have tested the election test, you should take a snapshot of your
three machines, as a base working condition:

    $ cd auth1
    auth1 $ vagrant snapshot take working-base
    auth1 $ cd  ..

    $ cd auth2
    auth2 $ vagrant snapshot take working-base
    auth2 $ cd  ..

    $ cd agora
    agora $ vagrant snapshot take working-base
    agora $ cd  ..

### Troubleshooting

#### Supervisor trouble

If the we loads but the form doesn't show up, and when you analyze traffic some
queries (for example  https://agora/authapi/api/auth-event/1/) return
"502 Bad Gateway", this might be because supervisor might be dead. This is a bug
that we don't know how to fix yet but has a simple solution: restart supervisor:

You can check that supervisor is down when this happens:


    $ cd agora
    agora $ vagrant ssh -c "sudo supervisorctl status"

        unix:///var/run/supervisor.sock no such file
        Connection to 127.0.0.1 closed.

If that's the case, restart it:

    $ cd agora
    agora $ vagrant ssh -c "sudo /etc/init.d/supervisor* restart"

Afterwards, supervisor status should return something like this, which is ok:

    $ cd agora
    agora $ vagrant ssh -c "sudo supervisorctl status"

        agora-elections                  RUNNING    pid 7665, uptime 0:00:04
        authapi                          RUNNING    pid 7663, uptime 0:00:04
        authapi_celery                   RUNNING    pid 7667, uptime 0:00:04
        sentry                           RUNNING    pid 7664, uptime 0:00:04
        sentry_celery                    RUNNING    pid 7666, uptime 0:00:04
        Connection to 127.0.0.1 closed.
