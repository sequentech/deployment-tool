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

from authapi.settings import *

DEBUG = {{config.authapi.debug}}

STATIC_ROOT = '/home/authapi/webstatic'
MEDIA_ROOT = '/home/authapi/webstatic/media'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'authapi',
        'USER': 'authapi',
        'PASSWORD': '{{config.eorchestra_password}}',
        'HOST': '{{ config.load_balancing.slave.master_hostname if not config.load_balancing.is_master else 'localhost' }}',
        'PORT': '5432',
    }
}

SHARED_SECRET = b'{{config.agora_elections.shared_secret}}'

SECRET_KEY = '{{ config.global_secret_key }}'
HOME_URL = "https://{{ config.agora_elections.domain }}/election/__EVENT_ID__/public/home"

ADMIN_AUTH_ID = 1

# If this option is true, then admin users can be deregistered and
# re-registered. Elections from deregistered users still are stored in the
# database. When a user re-registers after being de-registered, he will be
# able to modify fields that are not the email (in the case of email
# authentication) or phone number (in the case of phone-based auth) and once
# he is re-registered he will be able to see and manage elections created
# before he de-registered
#
# Users can only be deregistered while being logged in, using a call to
# authapi's url 'api/user/deregister/'. admin.py script in agora_elections
# can be used to ease executing this procedure.
#
# allowed values: true|false
# default: true
ALLOW_DEREGISTER = {% if config.authapi.allow_deregister %}True{% else %}False{% endif %}

# If this option is true, when an user tries to register and the user is
# already registered, authapi will return an error with the 'user_exists'
# codename. Otherwise, on error, authapi will always return the same generic
# error with 'invalid_credentials' codename.
SHOW_ALREADY_REGISTERED = {% if config.authapi.show_already_registered %}True{% else %}False{% endif %}

{% if config.authapi.sms.enabled %}
SMS_PROVIDER = "{{config.authapi.sms.provider}}"

SMS_DOMAIN_ID = "{{config.authapi.sms.domain_id}}"

SMS_LOGIN = "{{config.authapi.sms.login}}"

SMS_PASSWORD = "{{config.authapi.sms.sms_password}}"

SMS_URL = "{{config.authapi.sms.url}}"

SMS_SENDER_ID = "{{config.authapi.sms.sender_id}}"

SMS_SENDER_NUMBER = "{{config.authapi.sms.sender_number}}"

SMS_VOICE_LANG_CODE = {{config.authapi.sms.voice_lang_code}}

SMS_BASE_TEMPLATE = """{{config.authapi.sms.base_template}}"""

SMS_AUTH_CODE_URL = "https://{{ config.agora_elections.domain }}/election/__EVENT_ID__/public/login/__RECEIVER__"

{% endif %}

{% if config.authapi.email.enabled %}
DEFAULT_FROM_EMAIL = "{{config.authapi.email.default_from_email}}"

EMAIL_HOST = "{{config.authapi.email.email_host}}"

EMAIL_PORT = "{{config.authapi.email.email_port}}"

EMAIL_BASE_TEMPLATE = """{{config.authapi.email.base_template}}"""

EMAIL_BASE_TITLE_TEMPLATE = """{{config.authapi.email.base_title_template}}"""

EMAIL_AUTH_CODE_URL = "https://{{ config.agora_elections.domain }}/election/__EVENT_ID__/public/login/__RECEIVER__"

{% if 'email' == config.authapi.email.backend %}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
{% else %}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
{% endif %}

{% endif %}

AGORA_ELECTIONS_BASE = [
{% for agora_elections_base in config.authapi.agora_elections_base %}
"{{ agora_elections_base }}",
{% endfor %}
]

SMS_OTP_EXPIRE_SECONDS = {{config.authapi.sms_otp.expire_seconds}}

{% for extra_option in config.authapi.extra_options %}
{{extra_option}}
{% endfor %}
