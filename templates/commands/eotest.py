#!/usr/bin/env python

import requests
import json
import time

import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import SocketServer
import threading

import subprocess

import argparse
import sys
import __main__
from argparse import RawTextHelpFormatter

from datetime import datetime
import hashlib
import codecs
import traceback

import os.path
import os

PK_TIMEOUT = 60*10 # with three authorities 60 secons was not enough
TALLY_TIMEOUT = 3600*6 # 6 hours should be enough for what we do :-P
CERT = '/srv/certs/selfsigned/cert.pem'
KEY = '/srv/certs/selfsigned/key-nopass.pem'
DATA_DIR = "/srv/eotest/data"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

os.chdir(DATA_DIR)

# configuration
localPort = 8000
node = '/usr/bin/node'

def getPeerPkg(mypeerpkg):
    if mypeerpkg is None:
        mypeerpkg = subprocess.check_output(["/usr/bin/eopeers", "--show-mine"])
    if isinstance(mypeerpkg, basestring):
        return json.loads(mypeerpkg)
    else:
        return mypeerpkg

def getTallyData(mypeerpkg):
    mypeerpkg = getPeerPkg(mypeerpkg)
    localServer = mypeerpkg["hostname"]
    return {
        # 'election_id': electionId,
        "callback_url": "http://" + localServer + ":" + str(localPort) + "/receive_tally",
        "extra": [],
        "votes_url": "http://" + localServer + ":" + str(localPort) + "/",
        "votes_hash": "sha512://"
    }


def _apiUrl(path, pkg):
    '''
    Given a full api (without the initial '/') path and a package dict, returns
    a well formed url
    '''
    return "https://%(hostname)s:%(port)d/%(path)s" % dict(
        hostname=pkg["hostname"],
        port=pkg.get("port", 5000),
        path=path
    )

def grabAuthData(eopeers_dir, mypeerpkg, eopeers):
    mypeerpkg = getPeerPkg(mypeerpkg)

    if not os.path.isdir(eopeers_dir):
        print("%s is not a directory" % eopeers_dir)
        exit(1)

    l = os.listdir(eopeers_dir)
    if len(l) == 0:
        print("%s is an empty directory" % eopeers_dir)
        print("one authority")
        #exit(1)

    auths_data = [mypeerpkg]
    for fname in os.listdir(eopeers_dir):
        path = os.path.join(eopeers_dir, fname)
        with open(path, 'r') as f:
            auths_data.append(json.loads(f.read()))

    if eopeers is not None:
        if mypeerpkg['hostname'] not in eopeers:
            eopeers.append(mypeerpkg['hostname'])
        auths_data = [auth for auth in auths_data if auth['hostname'] in eopeers]
        hostnames = [a['hostname'] for a in auths_data]
        if len(hostnames) != len(eopeers):
            not_found = str(list(set(eopeers) - set(hostnames)))
            print("some peers were not found: %s" % not_found)
            exit(1)

    print("\nusing the following authorities:")
    i = 1
    ret_data = []
    for auth in auths_data:
        ret_data.append({
            "name": "Auth%d" %i,
            "orchestra_url": _apiUrl("api/queues", auth),
            "ssl_cert": auth["ssl_certificate"]
        })
        if i == 1:
            print(" 1. %s (this is us, acting as orchestra "
                  "director)" % auth['hostname'])
        else:
            print(" %d. %s" % (i, auth['hostname']))
        i += 1
    print("\n")
    return ret_data

def getStartData(eopeers_dir, mypeerpkg, eopeers):
    mypeerpkg = getPeerPkg(mypeerpkg)
    return {
        # "election_id": electionId,
        "is_recurring": False,
        "callback_url": "http://" + mypeerpkg["hostname"] + ":" + str(localPort) + "/key_done",
        "extra": [],
        "title": "Test election",
        "url": "https://example.com/election/url",
        "description": "election description",
        "questions_data": [{
            "question": "Who Should be President?",
            "tally_type": "ONE_CHOICE",
            # "answers": ["Alice", "Bob"],
            "answers": [
                {'a': 'ballot/answer',
                'details': '',
                'value': 'Alice'},
                {'a': 'ballot/answer',
                'details': '',
                'value': 'Bob'}
            ],
            "max": 1, "min": 0
        }],
        "voting_start_date": "2013-12-06T18:17:14.457000",
        "voting_end_date": "2013-12-09T18:17:14.457000",
        "authorities": grabAuthData(eopeers_dir, mypeerpkg, eopeers)
    }

# code

# thread signalling
cv = threading.Condition()

class ThreadingHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        print("> HTTP received " + self.path)
        if(self.path == "/exit"):
            self.send_response(204)
            cv.acquire()
            cv.done = True
            cv.notify()
            cv.release()
        else:
            SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        print("> HTTP received " + self.path + " (" + str(length) + ")")
        raw = self.rfile.read(length).decode('utf-8')
        data = json.loads(raw)

        # print(data)
        self.send_response(200)
        cv.acquire()
        cv.done = True
        cv.data = data
        cv.notify()
        cv.release()

# misc\utils.py
BUF_SIZE = 10*1024
def hash_file(file_path):
    '''
    Returns the hexdigest of the hash of the contents of a file, given the file
    path.
    '''
    hash = hashlib.sha512()
    f = open(os.path.join(DATA_DIR, file_path), 'r')
    for chunk in f.read(BUF_SIZE):
        hash.update(chunk)
    f.close()
    return hash.hexdigest()

def writeVotes(votesData, fileName):
    # forms/election.py:save
    votes = []
    for vote in votesData:
        data = {
            "a": "encrypted-vote-v1",
            "proofs": [],
            "choices": [],
            "voter_username": 'foo',
            "issue_date": str(datetime.now()),
            "election_hash": {"a": "hash/sha256/value", "value": "foobar"},
        }

        q_answer = vote['question0']
        data["proofs"].append(dict(
            commitment=q_answer['commitment'],
            response=q_answer['response'],
            challenge=q_answer['challenge']
        ))
        data["choices"].append(dict(
            alpha=q_answer['alpha'],
            beta=q_answer['beta']
        ))

        votes.append(data)

    # tasks/election.py:launch_encrypted_tally
    with codecs.open(os.path.join(DATA_DIR, fileName), encoding='utf-8', mode='w+') as votes_file:
        for vote in votes:
            # votes_file.write(json.dumps(vote['data'], sort_keys=True) + "\n")
            votes_file.write(json.dumps(vote, sort_keys=True) + "\n")

    # hash = hash_file(fileName)

    # return hash

def startServer(port):
    print("> Starting server on port " + str(port))
    server = ThreadingHTTPServer(('', port),RequestHandler)
    thread = threading.Thread(target = server.serve_forever)
    thread.daemon = True
    thread.start()

def startElection(electionId, url, data):
    data['election_id'] = electionId
    print("> Creating election " + electionId)
    cv.done = False
    r = requests.post(url, data=json.dumps(data), verify=False, cert=(CERT, KEY))
    print("> " + str(r))

def waitForPublicKey():
    start = time.time()
    cv.acquire()
    cv.wait(PK_TIMEOUT)
    pk = ''
    if(cv.done):
        diff = time.time() - start
        try:
            pk = cv.data['session_data'][0]['pubkey']
            print("> Election created " + str(diff) + " sec, public key is")
            print(pk)
        except:
            print("* Could not retrieve public key " + str(cv.data))
            print traceback.print_exc()
    else:
        print("* Timeout waiting for public key")
    cv.release()

    return pk

def doTally(electionId, url, data, votesFile, hash):
    data['votes_url'] = data['votes_url'] + votesFile
    data['votes_hash'] = data['votes_hash'] + hash
    data['election_id'] = electionId
    # print("> Tally post with " + json.dumps(data))
    print("> Requesting tally..")
    cv.done = False
    r = requests.post(url, data=json.dumps(data), verify=False, cert=(CERT, KEY))
    print("> " + str(r))

def waitForTally():
    start = time.time()
    cv.acquire()
    cv.wait(TALLY_TIMEOUT)
    ret = ''
    if(cv.done):
        diff = time.time() - start
        # print("> Received tally data (" + str(diff) + " sec) " + str(cv.data))
        print("> Received tally data " + str(diff) + " sec")
        if('tally_url' in cv.data['data']):
            ret = cv.data['data']
    else:
        print("* Timeout waiting for tally")
    cv.release()

    return ret

def downloadTally(url, electionId):
    fileName = electionId + '.tar.gz'
    path = os.path.join(DATA_DIR, fileName)
    print("> Downloading to %s" % path)
    with open(path, 'wb') as handle:
        request = requests.get(url, stream=True, verify=False, cert=(CERT, KEY))

        for block in request.iter_content(1024):
            if not block:
                break

            handle.write(block)






''' driving functions '''

def create(args):
    electionId = args.electionId
    startServer(localPort)
    mypeerpkg = getPeerPkg(args.mypeerpkg)
    startData = getStartData(args.eopeers_dir, args.mypeerpkg, args.peers)
    startUrl = _apiUrl("public_api/election", mypeerpkg)
    startElection(electionId, startUrl, startData)
    publicKey = waitForPublicKey()
    pkFile = 'pk' + electionId

    if(len(publicKey) > 0):
        print("> Saving pk to " + pkFile)
        with codecs.open(os.path.join(DATA_DIR, pkFile), encoding='utf-8', mode='w+') as votes_file:
            votes_file.write(json.dumps(publicKey))
    else:
        print("No public key, exiting..")
        exit(1)

    return pkFile

def encrypt(args):
    electionId = args.electionId
    pkFile = 'pk' + electionId
    votesFile = args.vfile
    votesCount = args.vcount
    ctexts = 'ctexts' + electionId
    # encrypting with vmnd
    if(args.vmnd):
        vmnd = "/usr/bin/vmnd.sh"
        vmndFile = os.path.join(DATA_DIR, "vmndCtexts" + electionId)
        if(votesCount == 0):
            votesCount = 10
        subprocess.call([vmnd, electionId, str(votesCount), vmndFile])
        if (os.path.isfile(vmndFile)):
            with open(vmndFile, 'r') as content_file:
                lines = content_file.readlines()
            votes = []

            for line in lines:
                fields = {
                    "is_vote_secret":True,"action":
                    "vote",
                    "issue_date":str(datetime.now()),
                    "unique_randomness":"foo",
                }
                lineJson = json.loads(line)
                lineJson["commitment"] = "foo"
                lineJson["response"] = "foo"
                lineJson["challenge"] = "foo"
                fields["question0"] = lineJson
                votes.append(fields)

            writeVotes(votes, ctexts)

        else:
            print("Could not read vmnd votes file " + vmndFile)
            exit(1)
    else:
        print("> Encrypting votes (" + votesFile + ", pk = " + pkFile + ", " + str(votesCount) + ")..")
        pkPath = os.path.join(DATA_DIR, pkFile)
        votesPath = os.path.join(DATA_DIR, votesFile)
        # if not present in data dir, use current directory
        if not (os.path.isfile(votesPath)):
            votesPath = votesFile
        if(os.path.isfile(pkPath)) and (os.path.isfile(votesPath)):
            output, error = subprocess.Popen([node, "encrypt.js", pkPath, votesPath, str(votesCount)], stdout = subprocess.PIPE).communicate()

            print("> Received Nodejs output (" + str(len(output)) + " chars)")
            parsed = json.loads(output)


            print("> Writing file to " + ctexts)
            writeVotes(parsed, ctexts)
        else:
            print("No public key or votes file, exiting..")
            exit(1)

def tally(args):
    if(args.command[0] == "tally"):
        startServer(localPort)

    electionId = args.electionId

    ctexts = 'ctexts' + electionId
    # need hash
    hash = hash_file(ctexts)
    print("> Votes hash is " + hash)
    tallyData = getTallyData(args.mypeerpkg)
    mypeerpkg = getPeerPkg(args.mypeerpkg)
    tallyUrl = _apiUrl('public_api/tally', mypeerpkg)
    doTally(electionId, tallyUrl, tallyData, ctexts, hash)
    tallyResponse = waitForTally()

    if('tally_url' in tallyResponse):
        print("> Downloading tally from " + tallyResponse['tally_url'])
        downloadTally(tallyResponse['tally_url'], electionId)
    else:
        print("* Tally not found in http data")

def full(args):
    electionId = args.electionId

    pkFile = create(args)

    if(os.path.isfile(os.path.join(DATA_DIR, pkFile))):
        encrypt(args)
        tally(args)
    else:
        print("No public key, exiting..")

def main(argv):
    if not (os.path.isdir(DATA_DIR)):
        print("> Creating data directory")
        os.makedirs(DATA_DIR)
    parser = argparse.ArgumentParser(description='EO testing script', formatter_class=RawTextHelpFormatter)
    parser.add_argument('command', nargs='+', default='full', help='''create: creates an election
encrypt <electionId>: encrypts votes
tally <electionId>: launches tally
full: does the whole process''')
    parser.add_argument('--eopeers-dir', help='directory with the eopeers packages to use as authorities', default = '/etc/eopeers/')
    parser.add_argument('--peers', nargs='+', default=None, help='list of authorities to pair with. defaults to all of them')
    parser.add_argument('--mypeerpkg', help='path to my peer package. if empty, calls to eopeers --show-mine', default = None)
    parser.add_argument('--vfile', help='json file to read votes from', default = 'votes.json')
    parser.add_argument('--vcount', help='number of votes to generate (generates duplicates if more than in json file)', type=int, default = 0)
    parser.add_argument('--vmnd', action='store_true', help='encrypts with vmnd')
    args = parser.parse_args()
    command = args.command[0]
    if hasattr(__main__, command):
        if(command == 'create') or (command == 'full'):
            args.electionId = str(time.time()).replace(".", "")
        elif(len(args.command) == 2):
            args.electionId = args.command[1]
        else:
            parser.print_help()
            exit(1)
        eval(command + "(args)")
    else:
        parser.print_help()

if __name__ == "__main__":
    main(sys.argv[1:])
