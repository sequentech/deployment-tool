import os
os.environ['SENTRY_CONF'] = "/home/sentry/sentry.conf.py"

# Bootstrap the Sentry environment
from sentry.runner import configure
configure()

# Create the org, team and project if needed
from sentry.models import Team, Project, ProjectKey, User, Organization, OrganizationMember

user = User.objects.get(pk=1)

name = 'AgoraVoting'
name2 = 'AuthApi'

if Organization.objects.filter(name=name).count() == 0:
    organization = Organization()
    organization.name = name
    organization.save()

    om = OrganizationMember()
    om.organization = organization
    om.role = 'owner'
    om.user = user
    om.save()

    team = Team()
    team.name = name
    team.organization = organization
    team.save()

    project = Project()
    project.team = team
    project.name = name2
    project.organization = organization
    project.save()
else:
    organization = Organization.objects.filter(name=name).all()[0]
    team = Team.objects.filter(name=name, organization=organization).all()[0]
    project =Project.objects.filter(team=team, name=name2, organization=organization).all()[0]

key = ProjectKey.objects.filter(project=project)[0]
dsn = key.get_dsn()
print(dsn)
