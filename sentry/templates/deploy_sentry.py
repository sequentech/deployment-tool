# sentry

# call to this function to update the globs globals variable: update(globals())
def update(globs):
    globs['RAVEN_CONFIG'] = dict(dsn='{{ dsn_contents.stderr }}')

    if 'raven.contrib.django.raven_compat' not in globs['INSTALLED_APPS']:
        globs['INSTALLED_APPS'] = globs['INSTALLED_APPS'] + (
            'raven.contrib.django.raven_compat',
        )

{% if config.sentry.msg_log %}
    globs['ADMINS'] = ( ('msg log', '{{ config.sentry.msg_log_email }}'), )
    globs['SERVER_EMAIL'] = '{{ config.authapi.server_email }}'
{% endif %}

    globs['LOGGING'] = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
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
            'handlers': ['sentry'],
            'propagate': False,
        },
        'authapi': {
            'level': 'INFO',
            'handlers': ['sentry'],
            'propagate': False,
        },
{% if config.sentry.msg_log %}
        'authapi.notify': {
            'level': 'INFO',
            'handlers': ['sentry', 'mail_admins'],
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
