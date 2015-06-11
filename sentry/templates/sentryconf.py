# Bootstrap the Sentry environment
from sentry.utils.runner import configure
configure("/home/sentry/sentry.conf.py")

# Do something crazy
from sentry.models import Team, Project, ProjectKey, User, Organization

user = User.objects.get(pk=1)

organization = Organization()
organization.name = 'AgoraVoting'
organization.owner = user
organization.save()

team = Team()
team.name = 'AgoraVoting'
team.organization = organization
team.save()

project = Project()
project.team = team
project.name = 'AuthApi'
project.organization = organization
project.save()

key = ProjectKey.objects.filter(project=project)[0]
dsn = key.get_dsn()

# writting the sentry configuration to deploy.conf
authapi_conf = '''
# sentry
RAVEN_CONFIG = {
    'dsn': '%s',
}
INSTALLED_APPS = INSTALLED_APPS + (
    'raven.contrib.django.raven_compat',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%%(levelname)s %%(asctime)s %%(module)s %%(process)d %%(thread)d %%(message)s'
        },
    },
    'handlers': {
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
'''

with open('/tmp/authapi.sentry', 'w') as f:
    f.write(authapi_conf % dsn)
