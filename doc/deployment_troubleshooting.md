# Deployment troubleshooting

## 1. Problems when creating the election

This is usually a problem with election authorities. Unfortunately, most of the
issues related to election authorities do not get reported to the user nor the
superadmins, although it's also true that most of these issues are solved when
doing the deployment.

To debug and analyze the situation, you can use the following commands in the
election authorities or the agora server:

1. See if the requests are reaching to nginx reading its log:

    $ sudo tail -f /var/log/nginx/access.log

nginx is in charge of filtering and accepting only https requests from http
clients (i.e. other "eopeers" or "agora" servers) whose client tls certificate
is installed in the peer.

If requests are being received but rejected with status 401 Unauthorized, it's
usually because:

a) the client TLS certificate has not been correctly installed, in which case
you just need to install the eopeer package (and restart nginx)

b) the client TLS certificate has correctly been installed, but it hasn't been
applied because you forgot to restart nginx with:

    $ service nginx restart

If on the other hand the requests are reaching to nginx but somehow are not
being processed, this is usually because previously an error happened during the
processing of an action of an election and the processing of the action was
never marked to a finished state, and election-orchestra is configured to
execute only one task at once. There's an easy way to solve this isssue; just
restart election-orchestra:

    $ supervisorctl restart eorchestra

2. You should also take a look at election-orchestra log:

    $ sudo supervisorctl tail -f eorchestra

election-orchestra is the software that organizes the creation of the keys
and the tallying of the election inside election authority servers,
communicating with other authorities and the agora servers.

You might find this kind of error in the eorchestra log:

    ConnectionError: HTTPConnectionPool(host='agora', port=14443): Max retries exceeded with url: /api/election/103/keydone (Caused by <class 'socket.error'>: [Errno 110] Connection timed out)

This happens when election keys have been created, but the last step, which is
to send the public keys to the requester agora server, has failed. This might
have happened because the agora TLS certificate is correctly installed (with
the peer package), but the ip address in the peer package was invalid, for
example because the communication with the agora server should be through its
private ip-address and it's been configured to be done through its public ip, or
viceversa. If it's the former, what you'd do is:

    # generate the correct agora peer package, with the private ip address
    agoraServer $ sudo eopeers --show-mine --private > agora.pkg

    # copy the agora peer package to the election authorities
    scp blah blah

    # uninstall the old agora peer package, install the new one and reinstall
    # nginx
    authX $ sudo eopeers --uninstall agora
    authX $ sudo eopeers --install agora.pkg && sudo service nginx restart

An alternative way of correcting the ip-address issue is to just add another
alias directly in /etc/hosts. This can be done in the deployment config.yml file
in the "config.hosts" variable.

3. Take a look at agora-elections log:

    $ sudo supervisorctl tail -f agora-elections

agora-elections is the application run in agora web servers that is in charge of
collecting cast ballots (the electronic ballot box) and also connecting with
election authorities to trigger the creation of election keys and launching
the tally.

When you launch an election, it might inmmediatly fail if the agora web server
doesn't have the election eopeer packages correctly installed. Please check
that:

a) The authority packages are installed with:

    $ sudo eopeers --list

b) The authority packages are installed with the correct ip-addresses. Bear in
mind that they might be installed with the public-ip address and maybe they
should be installed with the public ip address or viceversa. You can see a peer
package installed ip-address with:

    $ sudo eopeers --list <NAME>

c) check that the director authority peer package, which is the authority that
orchestrates the communication with other authorities, has been installed with
the eopeers "--keystore /home/agoraelections/keystore.jks" parameter. This is
needed because the TLS certificate of this authority needs to be accessible not
only to nginx but also directly to agora-elections.

Also, if you ever need to uninstall the peer package of this election authority,
remember to do --uninstall with the
"--keystore /home/agoraelections/keystore.jks" parameter.

d) Check that you have restarted both nginx and agora-elections if you have
changed any peer package:

    $ sudo supevisorctl restart agora-elections && sudo service nginx restart

e) Check that the list of election authorities are correctly configured in
agora-elections in the file
/home/agoraelections/agora-elections/conf/application.local.conf. This is
/configured during deployment in the "config.authorities", "config.director" and
"config.auths" variables in "config.yml".

4. Bear in mind that if you are using a production environment deployment, you
will have two or more front-end web servers with agora-elections. This means
that any of these servers might connect with the election authorities. The
configuration of the election authorities in that case is that one of them is
deemed to be the master agora server, and even though any of those agora servers
(with different private ip addresses) might be the initiator of a request to
the director election authority, the callback url will always point to the
same master agora server ip address. Also, note that the TLS certificate of
all the agora servers will be the same.

## 2. The election tally never succeeds

a) If the election public keys are correctly created, this means that the
connection between election authorities and the agora servers are usually all
ok; except for a couple things:

This usually happens when an election authority that is not the director
election authority hasn't got correctly configured the ip address or TLS
certificate of the agora server, and thus it has failed to download the list of
ballots from that server. This can be checked looking at the "eorchestra" log
in that election authority:

    authX $ sudo supervisorctl tail -f eorchestra

Or taking a look at nginx log in the agora server, in which the request would
not reach because it's going to another ip address:

    $ sudo tail -f /var/log/nginx/access.log

Note that this issue can also happen if in the agora server's nginx log the
request is logged (and thus the server is being reached) but with status
401 Unauthorized because the agora web server hasn't got properly configured
the TLS certificate of that election authority. The TLS certificate is included
in the peer package of the election authority.

To solve peer packages problems, see section 1.

b) If there is an error during the tally of plaintexts of the ballots (i.e.
after the anonymization and decryption step done by the election authorities).

In some rare cases, if there's an issue in agora-results configuration or a bug
in agora-results or agora-tally, this might happen. To detect this issue, take
a look at the log in agora-elections when receiving the plaintexts of the
ballots when calculating the tally:

    agora $ sudo supervisorctl tail -f agora-elections

## 3. Supervisor is not running

If the login page (/admin/login) loads but the form doesn't show up, and when
you analyze traffic some queries (for example  https://agora/authapi/api/auth-event/1/) return
"502 Bad Gateway", this might be because supervisor is dead. This is a bug
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

## 4. Problems provisioning

Sometimes the provisioning fails. This can be related to some syntax changes on
ansible's playbooks format. Check that you have Ansible 2.x or superior. If you
are using vagrant to provision a virtual machine, you need to install ansible 2.x 
on the host machine, not on the guest.

On Ubuntu, you can install the latest version of Ansible by executing:

    $ sudo apt-get install software-properties-common pwgen -y
    $ sudo apt-add-repository ppa:ansible/ansible -y
    $ sudo apt-get update
    $ sudo apt-get install ansible -y