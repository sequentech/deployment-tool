# This file is part of agora-dev-box.
# Copyright (C) 2014-2016  Agora Voting SL <agora@agoravoting.com>

# agora-dev-box is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# agora-dev-box  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with agora-dev-box.  If not, see <http://www.gnu.org/licenses/>.

# debug, set to false on production deployment
DEBUG = False

# see https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196
SQLALCHEMY_TRACK_MODIFICATIONS = False

ROOT_URL = 'https://{{ config.host }}:{{ config.port }}/api/queues'

# URL to our HTTP server
VFORK_SERVER_URL = 'http://{{ config.host }}'

VFORK_SERVER_PORT_RANGE = {{ config.vfork_server_ports }}

# Socket address given as <hostname>:<port> to our hint server.
# A hint server is a simple UDP server that reduces latency and
# traffic on the HTTP servers.
VFORK_HINT_SERVER_SOCKET = '{{ config.host }}'

VFORK_HINT_SERVER_PORT_RANGE = {{ config.vfork_hint_server_ports }}

import os
ROOT_PATH = os.path.split(os.path.abspath(__file__))[0]

# SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/db.sqlite' % ROOT_PATH
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2:///eorchestra'

PRIVATE_DATA_PATH = os.path.join(ROOT_PATH, 'datastore/private')
PUBLIC_DATA_PATH = '/srv/election-orchestra/server1/public'
PUBLIC_DATA_BASE_URL = 'https://{{ config.host }}:{{ config.port }}/public_data'


# security configuration
SSL_CERT_PATH = '{{ config.http.tls_cert_path }}'
SSL_KEY_PATH = '{{ config.http.tls_cert_key_path }}'
SSL_CALIST_PATH = '{{ config.http.tls_calist_path }}'
ALLOW_ONLY_SSL_CONNECTIONS = True
AUTOACCEPT_REQUESTS = {{ config.auto_mode }}

KILL_ALL_VFORK_BEFORE_START_NEW = True

# Maximum number of questions per election
MAX_NUM_QUESTIONS_PER_ELECTION = {{ config.election_limits.max_num_questions }}

QUEUES_OPTIONS = {
    'vfork_queue': {
        'max_threads': 1,
    }
}
