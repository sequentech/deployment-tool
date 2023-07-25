# This file is part of deployment-tool.
# Copyright (C) 2014-2016  Sequent Tech Inc <legal@sequentech.io>

# deployment-tool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# deployment-tool  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with deployment-tool.  If not, see <http://www.gnu.org/licenses/>.

from iam.settings import *
from celery import signals

@signals.setup_logging.connect
def on_celery_setup_logging(**kwargs):
    pass

USE_TZ = True

TIMEZONE = '{{ config.params.timezone | default('UTC') }}'

DEBUG = {{config.iam.debug}}

_DEFAULT_LOGGING_LEVEL = 'DEBUG'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': _DEFAULT_LOGGING_LEVEL,
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S%z'
        },
    },
    'handlers': {
        'console': {
            'level': _DEFAULT_LOGGING_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'iam': {
            'level': _DEFAULT_LOGGING_LEVEL,
            'handlers': ['console'],
            'propagate': False,
        },
        'celery': {
            'handlers': ['console'],
            'level': _DEFAULT_LOGGING_LEVEL,
            'propagate': False
        },
        'raven': {
            'level': _DEFAULT_LOGGING_LEVEL,
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': _DEFAULT_LOGGING_LEVEL,
            'handlers': ['console'],
            'propagate': False,
        },
    }
}

STATIC_ROOT = '/home/iam/webstatic'
MEDIA_ROOT = '/home/iam/webstatic/media'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'iam',
        'USER': 'iam',
        'PASSWORD': '{{config.election_orchestra.eorchestra_password}}',
        'HOST': '{{ config.load_balancing.slave.master_hostname if not config.load_balancing.is_master else 'localhost' }}',
        'PORT': '5432',
    }
}

SHARED_SECRET = b'{{config.ballot_box.shared_secret}}'

TIMEOUT = {{config.iam.auth_token_expiration_seconds}}

ADMIN_TIMEOUT = {{config.iam.admin_auth_token_expiration_seconds}}

SECRET_KEY = '{{ config.global_secret_key }}'
HOME_URL = "https://{{ config.ballot_box.domain }}/election/__EVENT_ID__/public/home"

ADMIN_AUTH_ID = 1

# Allow admin users registration
# Allowed values: True|False
# Default: False
ALLOW_ADMIN_AUTH_REGISTRATION = {% if config.iam.allow_admin_registration %}True{% else %}False{% endif %}

# If this option is true, then admin users can be deregistered and
# re-registered. Elections from deregistered users still are stored in the
# database. When a user re-registers after being de-registered, he will be
# able to modify fields that are not the email (in the case of email
# authentication) or phone number (in the case of phone-based auth) and once
# he is re-registered he will be able to see and manage elections created
# before he de-registered
#
# Users can only be deregistered while being logged in, using a call to
# iam's url 'api/user/deregister/'. admin.py script in ballot_box
# can be used to ease executing this procedure.
#
# allowed values: true|false
# default: true
ALLOW_DEREGISTER = {% if config.iam.allow_deregister %}True{% else %}False{% endif %}

# For admins:
# Allow sending custom html in the email messages sent from the admin console.
# Allowed values: True|False
# Default: False
ALLOW_HTML_EMAILS = {% if config.iam.allow_html_emails %}True{% else %}False{% endif %}

# If this option is true, when an user tries to register and the user is
# already registered, iam will return an error with the 'user_exists'
# codename. Otherwise, on error, iam will always return the same generic
# error with 'invalid_credentials' codename.
SHOW_ALREADY_REGISTERED = {% if config.iam.show_already_registered %}True{% else %}False{% endif %}

{% if config.iam.sms.enabled %}
SMS_PROVIDER = "{{config.iam.sms.provider}}"

SMS_DOMAIN_ID = "{{config.iam.sms.domain_id}}"

SMS_LOGIN = "{{config.iam.sms.login}}"

SMS_PASSWORD = "{{config.iam.sms.sms_password}}"

SMS_URL = "{{config.iam.sms.url}}"

SMS_SENDER_ID = "{{config.iam.sms.sender_id}}"

SMS_SENDER_NUMBER = "{{config.iam.sms.sender_number}}"

SMS_VOICE_LANG_CODE = {{config.iam.sms.voice_lang_code}}

SMS_BASE_TEMPLATE = """{{config.iam.sms.base_template}}"""

SMS_AUTH_CODE_URL = "https://{{ config.ballot_box.domain }}/election/__EVENT_ID__/public/login/__RECEIVER__"

{% endif %}

{% if config.iam.email.enabled %}
from django.core.mail.utils import DNS_NAME
DNS_NAME._fqdn = "{{ config.ballot_box.domain }}"

DEFAULT_FROM_EMAIL = "{{config.iam.email.default_from_email}}"

EMAIL_HOST = "{{config.iam.email.email_host}}"

EMAIL_PORT = "{{config.iam.email.email_port}}"

EMAIL_BASE_TEMPLATE = """{{config.iam.email.base_template}}"""

EMAIL_BASE_TITLE_TEMPLATE = """{{config.iam.email.base_title_template}}"""

EMAIL_AUTH_CODE_URL = "https://{{ config.ballot_box.domain }}/election/__EVENT_ID__/public/login/__RECEIVER__"

{% if config.ballot_box.enforce_state_controls %}
ENFORCE_STATE_CONTROLS = True
{% else %}
ENFORCE_STATE_CONTROLS = False
{% endif %}


{% if 'email' == config.iam.email.backend %}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
{% else %}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
{% endif %}

{% endif %}

SEQUENT_ELECTIONS_BASE = [
{% for ballot_box_base in config.iam.ballot_box_base %}
"{{ ballot_box_base }}",
{% endfor %}
]

SMS_OTP_EXPIRE_SECONDS = {{config.iam.sms_otp.expire_seconds}}

OPENID_CONNECT_PROVIDERS_CONF = [
{% for provider in config.iam.openid_connect_providers %}
      dict(
        public_info = dict(
{% for key, value in provider.public_info.items() %}
          {{key}}="{{value}}"{% if not loop.last %},{% endif %}

{% endfor %}
        ),
        private_config = dict(
{% for key, value in provider.private_config.items() %}
          {{key}}="{{value}}"{% if not loop.last %},{% endif %}
{% endfor %}

        )
      ){% if not loop.last %},{% endif %}
{% endfor %}

]

OTL_URL = "https://{{ config.ballot_box.domain }}/election/__EVENT_ID__/public/otl/__SECRET__"

ALT_AUTH_BASE_URL = "https://{{ config.ballot_box.domain }}/election/__EVENT_ID__/public/login-alt/__AUTH_METHOD_ID__"

# This is the command to be executed to launch a self-test
TASK_SELF_TEST_COMMAND = [
    "sudo", "-u", "ui_user", "/home/ui_user/launch_selftest.sh"
]

ENABLE_MULTIPLE_TALLIES = {{config.enable_multiple_tallies}}

AWS_SNS_MESSAGE_ATTRIBUTES = {
{% for key, value in config.iam.aws.sns_message_attributes.items() %}
    "{{key}}": {{value}}{% if not loop.last %},{% endif %}

{% endfor %}

}

{% for extra_option in config.iam.extra_options %}
{{extra_option}}
{% endfor %}


