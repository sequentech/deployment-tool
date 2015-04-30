# Ansible script to deploy an Agora server

## How to run it:

 * New vagrant virtual machine:
 $ vagrant up
 $ vagrant ssh

 * Remote server:
    * Create a inventory file with one server per line
      (http://docs.ansible.com/intro_inventory.html)
    * Run the playbook (NOTE: it requires at least ansible version 1.7.2!):
    $ ansible-playbook -i inventory playbook.yml

## This script deploys:

 * Agora authority:
   * election-orchestra
   * vfork
 * Agora ballotbox
   * auth-api
   * agora-core-view
   * agora-elections

## How to deploy an Auth:

 * Modify the config.yml
 * use the auth playbook:

```
    $ cp other-playbooks/playbook.auth.yml playbook.yml
```

 * Run the ansible (with vagrant or with an inventory):

```
    $ vagrant up
```

 * ssh to your deployed auth and link with other authorities with eopeers:

```
    $ vagrant ssh
    # eopeers --show-mine
    # eopeers --install authx.pkg
    # eopeers --list
```

 * Run the eotest to check that authorities are well connected:

```
    # eotest full --vmnd --vcount 100
```

 * If all is ok you should get an output like this:
```
root@agoravoting-eovm3:/home/vagrant# eotest full --vmnd --vcount 100
> Starting server on port 8000

using the following authorities:
 1. agoravoting-eovm3 (this is us, acting as orchestra director)
 2. agoravoting-eovm2

> Creating election 1880
> <Response [202]>
> HTTP received /key_done (2678)
192.168.0.3 - - [13/Jan/2015 18:21:52] "POST /key_done HTTP/1.1" 200 -
> Election created 14.4512028694 sec, public key is
{u'q': u'24792774508736884642868649594982829646677044143456685966902090450389126928108831401260556520412635107010557472033959413182721740344201744439332485685961403243832055703485006331622597516714353334475003356107214415133930521931501335636267863542365051534250347372371067531454567272385185891163945756520887249904654258635354225185183883072436706698802915430665330310171817147030511296815138402638418197652072758525915640803066679883309656829521003317945389314422254112846989412579196000319352105328237736727287933765675623872956765501985588170384171812463052893055840132089533980513123557770728491280124996262883108653723', u'p': u'49585549017473769285737299189965659293354088286913371933804180900778253856217662802521113040825270214021114944067918826365443480688403488878664971371922806487664111406970012663245195033428706668950006712214428830267861043863002671272535727084730103068500694744742135062909134544770371782327891513041774499809308517270708450370367766144873413397605830861330660620343634294061022593630276805276836395304145517051831281606133359766619313659042006635890778628844508225693978825158392000638704210656475473454575867531351247745913531003971176340768343624926105786111680264179067961026247115541456982560249992525766217307447', u'y': u'33596846789895155637256129820064142269294724065281480400646865970595001022185405454429683608456853809592978160603059225197473912903331423062102451046747626531950921063935870715414258013375087997330610394411246982488297210003867734470629111073636707618789145839148646295760182878231530928003509850572037330088112374093553037495441567414141201886043051029709506900202260708016401550587268785435787425187863785855754275150522063906228131764762579010752218890549825260403533792836130279555791822148381603652015112123584709003751979497444616823350208603814650040108904614982112539407723211631944761612619487454380682295448', u'g': u'27257469383433468307851821232336029008797963446516266868278476598991619799718416119050669032044861635977216445034054414149795443466616532657735624478207460577590891079795564114912418442396707864995938563067755479563850474870766067031326511471051504594777928264027177308453446787478587442663554203039337902473879502917292403539820877956251471612701203572143972352943753791062696757791667318486190154610777475721752749567975013100844032853600120195534259802017090281900264646220781224136443700521419393245058421718455034330177739612895494553069450438317893406027741045575821283411891535713793639123109933196544017309147'}
> Saving pk to pk1880
> vmnd.sh Executing vmnd -i json /home/eorchestra/election-orchestra/datastore/private/1880/*/protInfo.xml /home/eorchestra/election-orchestra/datastore/private/1880/*/publicKey_json 100 /srv/eotest/data/vmndCtexts1880
> Votes hash is bkhhW7z92eZOZ_NKqkCyTHh9L5oO4S9TDrjbMydreLQ=
> Requesting tally..
> <Response [202]>
> HTTP received /ctexts1880
192.168.0.4 - - [13/Jan/2015 18:21:54] "GET /ctexts1880 HTTP/1.1" 200 -
> HTTP received /ctexts1880
192.168.0.3 - - [13/Jan/2015 18:21:54] "GET /ctexts1880 HTTP/1.1" 200 -
> HTTP received /receive_tally (255)
192.168.0.3 - - [13/Jan/2015 18:22:12] "POST /receive_tally HTTP/1.1" 200 -
> Received tally data 18.6216800213 sec
> Downloading tally from https://agoravoting-eovm3:5000/public_data/1880/tally.tar.gz
> Downloading to /srv/eotest/data/1880.tar.gz
```


# License

Copyright (C) 2015 Agora Voting SL and/or its subsidiary(-ies).
Contact: legal@agoravoting.com

This file is part of the agora-core-view module of the Agora Voting project.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

Commercial License Usage
Licensees holding valid commercial Agora Voting project licenses may use this
file in accordance with the commercial license agreement provided with the
Software or, alternatively, in accordance with the terms contained in
a written agreement between you and Agora Voting SL. For licensing terms and
conditions and further information contact us at legal@agoravoting.com .

GNU Affero General Public License Usage
Alternatively, this file may be used under the terms of the GNU Affero General
Public License version 3 as published by the Free Software Foundation and
appearing in the file LICENSE.AGPL3 included in the packaging of this file, or
alternatively found in <http://www.gnu.org/licenses/>.

External libraries
This program distributes libraries from external sources. If you follow the
compilation process you'll download these libraries and their respective
licenses, which are compatible with our licensing.
