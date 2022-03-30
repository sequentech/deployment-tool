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

# sentry

# call to this function to update the globs globals variable: update(globals())
def update(globs):
    globs['RAVEN_CONFIG'] = dict(dsn='{{ dsn_contents.stdout }}')

    if 'raven.contrib.django.raven_compat' not in globs['INSTALLED_APPS']:
        globs['INSTALLED_APPS'] = globs['INSTALLED_APPS'] + (
            'raven.contrib.django.raven_compat',
        )

{% if config.sentry.msg_log %}
    globs['ADMINS'] = ( ('msg log', '{{ config.sentry.msg_log_email }}'), )
    globs['SERVER_EMAIL'] = '{{ config.iam.server_email }}'
{% endif %}

    globs['LOGGING'] = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry', 'console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
{% if config.sentry.msg_log %}
        'mail_admins': {
            'level': 'INFO',
            'class': 'django.utils.log.AdminEmailHandler'
        },
{% endif %}
        'sentry': {
            'level': 'INFO',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'level': 'ERROR',
            'handlers': ['sentry', 'console'],
            'propagate': False,
        },
        'iam': {
            'level': 'DEBUG',
            'handlers': ['sentry', 'console'],
            'propagate': False,
        },
{% if config.sentry.msg_log %}
        'iam.notify': {
            'level': 'INFO',
            'handlers': ['sentry', 'mail_admins', 'console'],
            'propagate': False,
        },
{% endif %}
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
