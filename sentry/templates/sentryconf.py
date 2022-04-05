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
