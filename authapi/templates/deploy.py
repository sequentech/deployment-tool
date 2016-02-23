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

{% if config.authapi.sms.enabled %}
SMS_PROVIDER = "{{config.authapi.sms.provider}}"

SMS_DOMAIN_ID = "{{config.authapi.sms.domain_id}}"

SMS_LOGIN = "{{config.authapi.sms.login}}"

SMS_PASSWORD = "{{config.authapi.sms.password}}"

SMS_URL = "{{config.authapi.sms.url}}"

SMS_SENDER_ID = "{{config.authapi.sms.sender_id}}"

SMS_VOICE_LANG_CODE = {{config.authapi.sms.voice_lang_code}}

SMS_BASE_TEMPLATE = """{{config.authapi.sms.base_template}}"""

SMS_AUTH_CODE_URL = "https://{{ config.agora_elections.domain }}/election/__EVENT_ID__/public/login"

{% endif %}

{% if config.authapi.email.enabled %}
DEFAULT_FROM_EMAIL = "{{config.authapi.email.default_from_email}}"

EMAIL_HOST = "{{config.authapi.email.email_host}}"

EMAIL_PORT = "{{config.authapi.email.email_port}}"

EMAIL_BASE_TEMPLATE = """{{config.authapi.email.base_template}}"""

EMAIL_AUTH_CODE_URL = "https://{{ config.agora_elections.domain }}/election/__EVENT_ID__/public/login/__RECEIVER__"

{% if 'email' == config.authapi.email.backend %}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
{% else %}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
{% endif %}

{% endif %}