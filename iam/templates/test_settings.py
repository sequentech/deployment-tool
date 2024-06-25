# This file is part of iam.
# Copyright (C) 2014-2020  Sequent Tech Inc <legal@sequentech.io>

# iam is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# iam  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with iam.  If not, see <http://www.gnu.org/licenses/>.

"""
Django settings for iam project.
For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
from datetime import timedelta

TESTING = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Celery config
class CeleryConfig:
    broker_url = "amqp://guest:guest@localhost:5672//"
    timezone = 'Europe/Madrid'
    beat_schedule = {
        'review_tallies': {
            'task': 'tasks.process_tallies',
            'schedule': timedelta(seconds=5),
            'args': []
        },
    }
    result_backend = 'cache'
    cache_backend = 'memory'
    task_always_eager = True
    task_eager_propagates = True

CELERY_CONFIG = CeleryConfig

USE_TZ = True

TIME_ZONE = 'Europe/Madrid'

ALLOW_DEREGISTER = True

ALLOW_HTML_EMAILS = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zct2c=hlij$^0xu0i8o6c^phjc!=m)r(%h90th0yyx9r5dm))+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

TIMEOUT = 300

ADMIN_TIMEOUT = 3000

ADMIN_AUTH_ID = 1

ALLOW_ADMIN_AUTH_REGISTRATION = False

# If this option is true, when an user tries to register and the user is
# already registered, iam will return an error with the 'user_exists'
# codename. Otherwise, on error, iam will always return the same generic
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
    'tasks',

    #3rd party
    'corsheaders',
    'django_nose',
)

PLUGINS = (
    # Add plugins here
)

if PLUGINS:
    INSTALLED_APPS += PLUGINS

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# change the test runner to the one provided by celery so that the tests that
# make use of celery work when ./manage.py test is executed
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

ROOT_URLCONF = 'iam.urls'
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

WSGI_APPLICATION = 'iam.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME', 'iam_test'),
        'USER': os.environ.get('POSTGRES_USER', 'iam_test'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', '{{config.election_orchestra.eorchestra_password}}'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
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
STATIC_PREVIEW_PATH = os.path.join(BASE_DIR, 'static', 'preview')

# cors
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
        'http://localhost:9001',
)

ENFORCE_STATE_CONTROLS = True

OPENID_CONNECT_PROVIDERS_CONF = []

# When a task is performed by launching a subprocess, the output of this process
# is going to be written to the database. We use this setting to prevent too
# many updates per second, by setting a minimum elapsed time between DB updates.
TASK_PROCESS_UPDATE_DEBOUNCE_SECS = 2.0

# This is the command to be executed to launch a self-test
TASK_SELF_TEST_COMMAND = ["/home/iam/launch_selftest.sh"]

# This is the command to be executed to kill a self-test
TASK_SELF_TEST_KILL_COMMAND = ["sudo", "/home/ui_user/kill_selftest.sh"]

# Default maximum amount of time in seconds that a task should last. After this,
# amount of time, the task is killed
TASK_DEFAULT_TIMEOUT_SECS = 60

ENABLE_CAPTCHA = True
PREGENERATION_CAPTCHA = 100

ENFORCE_STATE_CONTROLS = False

SMS_PROVIDER = "test"
SMS_DOMAIN_ID = ""
SMS_LOGIN = ""
SMS_PASSWORD = ""
SMS_URL = ""
SMS_SENDER_ID = ""
SMS_SENDER_NUMBER = ""
SMS_VOICE_LANG_CODE = ""

SMS_OTP_EXPIRE_SECONDS = 300

MAX_AUTH_MSG_SIZE = {
  "sms": 120,
  "email": 10000
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SMS_BASE_TEMPLATE = "__MESSAGE__ -- Sequent"

EMAIL_BASE_TEMPLATE = "__MESSAGE__\n\n -- Sequent https://sequentech.io"

EMAIL_BASE_TITLE_TEMPLATE = "__TITLE__ - Sequent"

HOME_URL = "https://sequent.example.com/#/election/__EVENT_ID__/public/home"
SMS_AUTH_CODE_URL = "https://sequent.example.com/#/election/__EVENT_ID__/public/login/__RECEIVER__"
EMAIL_AUTH_CODE_URL = "https://sequent.example.com/#/election/__EVENT_ID__/public/login/__RECEIVER__"
OTL_URL = "https://sequent.example.com/election/__EVENT_ID__/otl/__SECRET__"
ALT_AUTH_BASE_URL = "https://sequent.example.com/election/__EVENT_ID__/public/login/__AUTH_METHOD_ID__"

SEQUENT_ELECTIONS_BASE = []

SIZE_CODE = 8
MAX_GLOBAL_STR = 512
MAX_EXTRA_FIELDS = 15
MAX_ADMIN_FIELDS = 15
MAX_SIZE_NAME_EXTRA_FIELD = 1024

MAX_IMAGE_SIZE = 5 * 1024 * 1024 # 5 MB
IMAGE_STORE_PATH = os.path.join(BASE_DIR, 'imgfields')

ENABLE_MULTIPLE_TALLIES = False

{% set max_body_size_bytes = (config.http.max_body_size[:-1] | int) * 1024 * 1024 %}

DATA_UPLOAD_MAX_MEMORY_SIZE = {{  max_body_size_bytes }}

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
