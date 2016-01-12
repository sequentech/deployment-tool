# Bootstrap the Sentry environment
from sentry.utils.runner import configure
configure("/home/sentry/sentry.conf.py")

# Create the org, team and project if needed
from sentry.models import Team, Project, ProjectKey, User, Organization

user = User.objects.get(pk=1)

name = 'AgoraVoting'
name2 = 'AuthApi'

if Organization.objects.filter(name=name, owner=user).count() == 0:
    organization = Organization()
    organization.name = name
    organization.owner = user
    organization.save()

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
    organization = Organization.objects.filter(name=name, owner=user).all()[0]
    team = Team.objects.filter(name=name, organization=organization).all()[0]
    project =Project.objects.filter(team=team, name=name2, organization=organization).all()[0]

key = ProjectKey.objects.filter(project=project)[0]
dsn = key.get_dsn()
print(dsn)
