# Complete Sequent deployment system

This document describes the complete deployment of a Sequent system
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

- Ansible 2.1

Vagrant uses the host's ansible to do provisioning on the guest machines. 
Because of some changes in the format of playbooks, we need to use
Ansible 2.1. To install the latest ansible on an Ubuntu machine, execute:

    $ sudo apt-get install software-properties-common pwgen -y
    $ sudo apt-add-repository ppa:ansible/ansible-2.1 -y
    $ sudo apt-get update
    $ sudo apt-get install ansible=2.1* -y
    $ sudo apt-mark hold ansible

## deployment-tool

First of all we need to download the ansible deployment project:

    $ git clone https://github.com/sequentech/deployment-tool.git

Note: sometimes the 'next' branch has important updates. In case you want
to use the 'next' branch, do:

    $ cd deployment-tool/
    $ git checkout next
    $ cd .. 

## Servers

We need at least 3 servers to deploy a secure environment. We'll have two
authorities and then another server with the authentication (iam), the 
web interface (sequent-ui) and the ballot box (aogra\_elections).

The deployment is tested with ubuntu/trusty64, it should work with other
ubuntu distributions, but maybe the deployment needs some tweaks.

## Vagrant machines

If you have real machines you can skip this step, but be sure to modify
each config file to use your real IPs.

First of all we'll create the three servers we need with vagrant. Now copy the
deployment-tool folder three times with different names, one for each server:

    $ cp -r deployment-tool auth1
    $ cp -r deployment-tool auth2
    $ cp -r deployment-tool sequent

Then we can create each Vagrant machine. Note: if we want to assign more
memory or a change in the number of CPUs to the vagrant machines for a faster
installation, we can edit Vagrantfile and change v.memory (memory in MB)
and v.cpus (number of CPUs):

    $ cd auth1
    auth1 $ cp doc/devel/Vagrantfile.auth1 Vagrantfile && vagrant up --no-provision && vagrant ssh-config > ./vagrant.ssh.config && vagrant snapshot take zero
    auth1 $ cd .. 

    $ cd auth2
    auth2 $ cp doc/devel/Vagrantfile.auth2 Vagrantfile && vagrant up --no-provision && vagrant ssh-config > ./vagrant.ssh.config && vagrant snapshot take zero
    auth2 $ cd .. 

    $ cd sequent
    sequent $ cp doc/devel/Vagrantfile.sequent Vagrantfile && vagrant up --no-provision && vagrant ssh-config > ./vagrant.ssh.config && vagrant snapshot take zero
    sequent $ cd .. 

Now we've three basic Ubuntu 14.04.3 LTS (Trusty Tahr) machines connected with the following IPs:

 * auth1: 192.168.50.2
 * auth2: 192.168.50.3
 * sequent: 192.168.50.4

So you should add this to your local machine /etc/hosts to be able to access them by domain name:

    echo -e "192.168.50.2 local-auth1\n192.168.50.3 local-auth2\n192.168.50.4 sequent"  | sudo tee -a /etc/hosts

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

    $ cd sequent
    sequent $ cp doc/devel/sequent.config.yml config.yml
    sequent $ cp doc/devel/base.playbook.yml playbook.yml
    sequent $ vagrant provision
    sequent $ vagrant snapshot take base
 
## Authorities server

### Provisioning

We need to deploy the two authorities and connect them. The deployment
process is the same for both authorities.

    $ cd auth1
    auth1 $ cp doc/devel/auth.playbook.yml playbook.yml
    auth1 $ vagrant provision
    auth1 $ vagrant ssh -c "sudo eopeers --show-mine | tee /home/vagrant/auth1.pkg >/dev/null"
    auth1 $ scp -F vagrant.ssh.config default:/home/vagrant/auth1.pkg auth1.pkg
    auth1 $ cd .. 

    $ cd auth2
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
/srv/certs/selfsigned/ and we manage the authority communication and
certificate sharing with the eopeers tool. 

    $ cd auth1
    auth1 $ scp -F vagrant.ssh.config ../auth2/auth2.pkg default:/home/vagrant/auth2.pkg
    auth1 $ vagrant ssh -c "sudo eopeers --install /home/vagrant/auth2.pkg && sudo service nginx restart"
    auth1 $ cd .. 

    $ cd auth2
    auth2 $ scp -F vagrant.ssh.config ../auth1/auth1.pkg default:/home/vagrant/auth1.pkg
    auth2 $ vagrant ssh -c "sudo eopeers --install /home/vagrant/auth1.pkg && sudo service nginx restart"
    auth2 $ cd .. 
 
### Test the connection between the authorities 
 
A script is installed to test the real connection between the authorities.
Open two terminal windows. Open eolog in one of the terminal windows:

    $ cd auth2 
    auth2 $ vagrant ssh -c "sudo eolog"

Now run eotest in the other terminal window from the other auth server:

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

Let's provision the sequent server in a similar fashion as we did with the
authorities:

    $ cd sequent
    sequent $ cp doc/devel/sequent.playbook.yml playbook.yml
    sequent $ vagrant provision
    sequent $ vagrant ssh -c "sudo eopeers --show-mine --private-ip | tee /home/vagrant/sequent.pkg >/dev/null"
    sequent $ scp -F vagrant.ssh.config default:/home/vagrant/sequent.pkg sequent.pkg
    sequent $ cd .. 

### Connecting sequent server with authorities

The ballotbox should be able to communicate with the authorities. We'll
use local-auth1 as the director authority, but we need to add all 
authorities to our eopeers.

    $ cd auth1
    auth1 $ scp -F vagrant.ssh.config ../sequent/sequent.pkg default:/home/vagrant/sequent.pkg && vagrant ssh -c "sudo eopeers --install /home/vagrant/sequent.pkg; sudo service nginx restart"
    auth1 $ cd .. 

    $ cd auth2
    auth2 $ scp -F vagrant.ssh.config ../sequent/sequent.pkg default:/home/vagrant/sequent.pkg && vagrant ssh -c "sudo eopeers --install /home/vagrant/sequent.pkg; sudo service nginx restart"
    auth2 $ cd .. 

    $ cd sequent
    sequent $ scp -F vagrant.ssh.config ../auth1/auth1.pkg ../auth2/auth2.pkg default:/home/vagrant/
    sequent $ vagrant ssh -c "sudo eopeers --install /home/vagrant/auth1.pkg --keystore /home/ballotbox/keystore.jks; sudo eopeers --install /home/vagrant/auth2.pkg; sudo service nginx restart; sudo supervisorctl restart ballot-box"
    sequent $ cd .. 

After completing all these steps, we now have a complete Sequent Tech installation.

### Complete election test

You can open your broswer and make the rest of the election using the admin:

    https://sequent/admin/login

Use the default credentials:

    Email : admin@sequentech.io
    Authentication Code : QWERTY33

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

    $ cd sequent
    sequent $ vagrant snapshot take working-base
    sequent $ cd  ..

### Troubleshooting

For Troubleshooting please read the deployment_troubleshooting.md file.
