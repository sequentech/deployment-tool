# Ansible script to deploy an Agora server

## How to run it:

 * New vagrant virtual machine:
 $ vagrant up
 $ vagrant ssh

 * Remote server:
    * Create a inventory file with one server per line
      (http://docs.ansible.com/intro_inventory.html)
    * Run the playbook:
    $ ansible-playbook -i inventory playbook.yml

## This script deploys:

 * Agora authority:
   * election-orchestra
   * verificatum
 * Agora ballotbox
   * auth-api
   * agora-core-view
   * agora-elections
