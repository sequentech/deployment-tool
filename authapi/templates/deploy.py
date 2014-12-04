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
        'PASSWORD': 'authapi',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
