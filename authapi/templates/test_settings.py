# This file is part of authapi.
# Copyright (C) 2014-2016  Agora Voting SL <agora@agoravoting.com>

# authapi is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# authapi  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with authapi.  If not, see <http://www.gnu.org/licenses/>.

"""
Django settings for authapi project.
For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import djcelery
djcelery.setup_loader()

# Celery config
BROKER_URL = "amqp://guest:guest@localhost:5672//"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zct2c=hlij$^0xu0i8o6c^phjc!=m)r(%h90th0yyx9r5dm))+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ADMIN_AUTH_ID = 1

# If this option is true, when an user tries to register and the user is
# already registered, authapi will return an error with the 'user_exists'
# codename. Otherwise, on error, authapi will always return the same generic
# error with 'invalid_credentials' codename.
SHOW_ALREADY_REGISTERED = False

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # custom
    'api',
    'authmethods',
    'captcha',

    #3rd party
    'corsheaders',
    'djcelery',
    'django_nose',
)

PLUGINS = (
    # Add plugins here
)

if PLUGINS:
    INSTALLED_APPS += PLUGINS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wrap.LoggingMiddleware'
)

# change the test runner to the one provided by celery so that the tests that
# make use of celery work when ./manage.py test is executed
TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

ROOT_URLCONF = 'authapi.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'authapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'authapi',
        'USER': 'authapi',
        'PASSWORD': '{{config.eorchestra_password}}'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# cors
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
        'localhost:9001',
)

ENABLE_CAPTCHA = True
PREGENERATION_CAPTCHA = 100

SMS_PROVIDER = "test"
SMS_DOMAIN_ID = ""
SMS_LOGIN = ""
SMS_PASSWORD = ""
SMS_URL = ""
SMS_SENDER_ID = ""
SMS_VOICE_LANG_CODE = ""

MAX_AUTH_MSG_SIZE = {
  "sms": 120,
  "email": 10000
}

SMS_BASE_TEMPLATE = "__MESSAGE__ -- nVotes"

EMAIL_BASE_TEMPLATE = "__MESSAGE__\n\n -- nVotes https://nvotes.com"

EMAIL_BASE_TITLE_TEMPLATE = "__TITLE__ - nVotes"

HOME_URL = "https://agoravoting.example.com/#/election/__EVENT_ID__/public/home"
SMS_AUTH_CODE_URL = "https://agoravoting.example.com/#/election/__EVENT_ID__/public/login/__RECEIVER__"
EMAIL_AUTH_CODE_URL = "https://agoravoting.example.com/#/election/__EVENT_ID__/public/login/__RECEIVER__"

SIZE_CODE = 8
MAX_GLOBAL_STR = 512
MAX_EXTRA_FIELDS = 15
MAX_ADMIN_FIELDS = 15
MAX_SIZE_NAME_EXTRA_FIELD = 1024

MAX_IMAGE_SIZE = 5 * 1024 * 1024 # 5 MB
IMAGE_STORE_PATH = os.path.join(BASE_DIR, 'imgfields')

if not os.path.exists(IMAGE_STORE_PATH):
    os.mkdir(IMAGE_STORE_PATH)

if PLUGINS:
    import importlib
    for plugin in PLUGINS:
        mod = importlib.import_module("%s.test_settings" % plugin)
        to_import = [name for name in dir(mod) if not name.startswith('_')]
        locals().update({name: getattr(mod, name) for name in to_import})

# Auth api settings
from auth_settings import *

try:
    from custom_settings import *
except:
    pass
