# This file is just Python, with a touch of Django which means
# you can inherit and tweak settings to your hearts content.
from sentry.conf.server import *

import os.path

CONF_ROOT = os.path.dirname(__file__)

# You should not change this setting after your database has been created
# unless you have altered all schemas first
SENTRY_USE_BIG_INTS = True

# If you're expecting any kind of real traffic on Sentry, we highly recommend
# configuring the CACHES and Redis settings

###########
# General #
###########

# The administrative email for this installation.
# Note: This will be reported back to getsentry.com as the point of contact. See
# the beacon documentation for more information. This **must** be a string.

# SENTRY_ADMIN_EMAIL = 'your.name@example.com'
SENTRY_ADMIN_EMAIL = '{{ config.sentry_admin_user }}'

# Instruct Sentry that this install intends to be run by a single organization
# and thus various UI optimizations should be enabled.
SENTRY_SINGLE_ORGANIZATION = True

# for more information on DATABASES, see the Django configuration at:
# https://docs.djangoproject.com/en/1.6/ref/databases/
DATABASES = {
    'default': {
        # We suggest PostgreSQL for optimal performance
        'ENGINE': 'sentry.db.postgres',

        'NAME': 'sentry',
        'USER': 'sentry',
        'PASSWORD': '{{ config.sentry_db_password }}',
        'HOST': '{{ config.load_balancing.slave.master_hostname if not config.load_balancing.is_master else 'localhost' }}',
        'PORT': '5432',
    }
}

#########
# Redis #
#########

# Generic Redis configuration used as defaults for various things including:
# Buffers, Quotas, TSDB

SENTRY_REDIS_OPTIONS = {
    'hosts': {
        0: {
            'host': '127.0.0.1',
            'port': 6379,
        }
    }
}

#########
# Cache #
#########

# If you wish to use memcached, install the dependencies and adjust the config
# as shown:
#
#   pip install python-memcached
#
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': ['127.0.0.1:11211'],
#     }
# }
#
# SENTRY_CACHE = 'sentry.cache.django.DjangoCache'

SENTRY_CACHE = 'sentry.cache.redis.RedisCache'

#########
# Queue #
#########

# See http://sentry.readthedocs.org/en/latest/queue/index.html for more
# information on configuring your queue broker and workers. Sentry relies
# on a Python framework called Celery to manage queues.

CELERY_ALWAYS_EAGER = False
BROKER_URL = 'redis://localhost:6379'

###############
# Rate Limits #
###############

SENTRY_RATELIMITER = 'sentry.ratelimits.redis.RedisRateLimiter'

##################
# Update Buffers #
##################

# Buffers (combined with queueing) act as an intermediate layer between the
# database and the storage API. They will greatly improve efficiency on large
# numbers of the same events being sent to the API in a short amount of time.
# (read: if you send any kind of real data to Sentry, you should enable buffers)

SENTRY_BUFFER = 'sentry.buffer.redis.RedisBuffer'

##########
# Quotas #
##########

# Quotas allow you to rate limit individual projects or the Sentry install as
# a whole.

SENTRY_QUOTAS = 'sentry.quotas.redis.RedisQuota'

########
# TSDB #
########

# The TSDB is used for building charts as well as making things like per-rate
# alerts possible.

SENTRY_TSDB = 'sentry.tsdb.redis.RedisTSDB'

################
# File storage #
################

# Any Django storage backend is compatible with Sentry. For more solutions see
# the django-storages package: https://django-storages.readthedocs.org/en/latest/

SENTRY_FILESTORE = 'django.core.files.storage.FileSystemStorage'
SENTRY_FILESTORE_OPTIONS = {
    'location': '/tmp/sentry-files',
}

##############
# Web Server #
##############

ALLOWED_HOSTS = ['*']

# You MUST configure the absolute URI root for Sentry:
SENTRY_URL_PREFIX = 'http://{{ config.agora_elections_domain }}:{{ config.sentry_port }}'  # No trailing slash!

# If you're using a reverse proxy, you should enable the X-Forwarded-Proto
# header and uncomment the following settings
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SENTRY_WEB_HOST = '0.0.0.0'
SENTRY_WEB_PORT = {{ config.sentry_port }}
SENTRY_WEB_OPTIONS = {
    # 'workers': 3,  # the number of gunicorn workers
    # 'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},
}

###############
# Mail Server #
###############

# For more information check Django's documentation:
#  https://docs.djangoproject.com/en/1.3/topics/email/?from=olddocs#e-mail-backends

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'localhost'
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
EMAIL_PORT = 25
EMAIL_USE_TLS = False

# The email address to send on behalf of
SERVER_EMAIL = '{{ config.sentry_admin_user }}'

# If you're using mailgun for inbound mail, set your API key and configure a
# route to forward to /api/hooks/mailgun/inbound/
MAILGUN_API_KEY = ''

########
# etc. #
########

# If this file ever becomes compromised, it's important to regenerate your SECRET_KEY
# Changing this value will result in all current sessions being invalidated
SECRET_KEY = '{{ config.global_secret_key }}'
