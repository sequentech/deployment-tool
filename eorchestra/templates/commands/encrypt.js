var fs = require('fs');

// otherwise one of the scripts complains
var navigator = {
  "appName": "foo"
};

filedata = fs.readFileSync('agora-ciudadana/agora_site/static/js/agora/libs/crypto/jsbn.js','utf8');
eval(filedata);

filedata = fs.readFileSync('agora-ciudadana/agora_site/static/js/agora/libs/crypto/jsbn2.js','utf8');
eval(filedata);

filedata = fs.readFileSync('agora-ciudadana/agora_site/static/js/agora/libs/crypto/bigint.js','utf8');
eval(filedata);

filedata = fs.readFileSync('agora-ciudadana/agora_site/static/js/agora/libs/crypto/class.js','utf8');
eval(filedata);

filedata = fs.readFileSync('agora-ciudadana/agora_site/static/js/agora/libs/crypto/elgamal.js','utf8');
eval(filedata);

filedata = fs.readFileSync('agora-ciudadana/agora_site/static/js/agora/libs/crypto/random.js','utf8');
eval(filedata);

filedata = fs.readFileSync('agora-ciudadana/agora_site/static/js/agora/libs/crypto/sha1.js','utf8');
eval(filedata);
filedata = fs.readFileSync('agora-ciudadana/agora_site/static/js/agora/libs/crypto/sha2.js','utf8');
eval(filedata);

filedata = fs.readFileSync('agora-ciudadana/agora_site/static/js/libs/json2.js','utf8');
eval(filedata);

var sjcl = require('./agora-ciudadana/agora_site/static/js/agora/libs/crypto/sjcl.js');
var moment = require('./agora-ciudadana/agora_site/static/js/libs/moment.js');

// FIXME copied from voting_booth.js as it is a hassle to import the whole agora view structure
var encryptAnswer = function(pk_json, plain_answer) {

    var pk = ElGamal.PublicKey.fromJSONObject(pk_json);
    var plaintext = new ElGamal.Plaintext(BigInt.fromInt(plain_answer), pk, true);
    var randomness = Random.getRandomInteger(pk.q);
    var ctext = ElGamal.encrypt(pk, plaintext, randomness);
    var proof = plaintext.proveKnowledge(ctext.alpha, randomness, ElGamal.fiatshamir_dlog_challenge_generator);
    var ciphertext =  ctext.toJSONObject();
    var json_proof = proof.toJSONObject();
    var enc_answer = {
        alpha: ciphertext.alpha,
        beta: ciphertext.beta,
        commitment: proof.commitment,
        response: proof.response,
        challenge: proof.challenge
    };

    var verified = ctext.verifyPlaintextProof(proof, ElGamal.fiatshamir_dlog_challenge_generator);
    console.warn("> Node: proof verified = " + new Boolean(verified).toString());
    return enc_answer;
}

var updateTally = function(tally, vote) {
    if(!(vote in tally)) {
        tally[vote] = 1;
    }
    else {
        tally[vote] = tally[vote] + 1;
    }
}

if(process.argv.length < 4) {
    console.error("* Node: Need public key and votes.json file args to encrypt votes");
    process.exit(1);
}
else {
    try {
        console.warn("> Node: reading pk ");

        var pkStr = fs.readFileSync(process.argv[2], 'utf8');
        var pk = JSON.parse(pkStr);

        var tally = {};

        // voting_booth.js:castVote
        var ballots = [];
        var answersStr = fs.readFileSync(process.argv[3], 'utf8');
        var answers = JSON.parse(answersStr);

        for(var i = 0; i < answers.length; i++) {
            var answer = [answers[i]];
            updateTally(tally, answers[i]);
            console.warn('> Node: encrypting answer \'' + answer + '\'');
            ballot = {
              'is_vote_secret': true,
              'action': 'vote'
            };
            ballot['issue_date'] = moment().format();
            var random = sjcl.random.randomWords(5, 0);
            var rand_bi = new BigInt(sjcl.codec.hex.fromBits(random), 16);
            ballot['unique_randomness'] = rand_bi.toRadix(16);
            ballot['question0'] = encryptAnswer(pk,  BigInt.fromInt(answer));

            ballots.push(ballot);
        }

        if(process.argv.length == 5) {
            var totalVotes = process.argv[4];
            if(totalVotes > answers.length) {
                console.warn('> Node: duplicating votes to reach ' + totalVotes);
                for(var i = answers.length; i < totalVotes; i++) {
                    var nextVote = Math.floor((Math.random()*answers.length));
                    // console.warn('> Node: duplicating ' + answers[nextVote]);
                    updateTally(tally, answers[nextVote]);
                    ballots.push(ballots[nextVote]);
                }
            }
        }
        var serialized = JSON.stringifyCompat(ballots)
        console.warn('> Node: tally = ' + JSON.stringifyCompat(tally));
        console.warn('> Node: outputting votes..');
        console.log(serialized);
    }
    catch(err) {
        console.error("* Exception encrypting votes " + err);
        process.exit(1)
    }
}