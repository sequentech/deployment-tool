from authapi.settings import *

DEBUG = False

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

SHARED_SECRET = b'{{config.agora_elections_shared_secret}}'

SECRET_KEY = '{{ config.global_secret_key }}'
