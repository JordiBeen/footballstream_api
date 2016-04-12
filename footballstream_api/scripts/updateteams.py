import logging
import os
import sys

from pyramid.paster import (
    get_appsettings,
    setup_logging)

import requests

from sqlalchemy import engine_from_config

import transaction

from ..models import merge, persist
from ..models.meta import Base, DBSession
from ..models.competition import Competition, get_competition  # noqa
from ..models.team import Team, get_team, list_teams  # noqa

log = logging.getLogger(__name__)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s template.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    update_teams(settings)
    print('Teams successfully updated')


def update_teams(settings):
    api_key = settings['football-api.key']
    api_url = settings['football-api.url']

    for team in list_teams():
        log.info('Getting info for team with id: {}'
                 .format(team.external_id))
        api_endpoint = "/team/{}".format(team.external_id)

        payload = {'Authorization': api_key}
        request = requests.get(api_url + api_endpoint, params=payload)
        response = request.json()

        # Check if this object actually has a team or is
        # a faux object
        if request.status_code != 200:
            continue

        with transaction.manager:
            # Does the team exist yet?
            team = get_team(external_id=response['team_id'])

            # If not, we create a new team
            if not team:
                log.info("Team does not yet exist, creating team")
                team = Team()
                team.external_id = response['team_id']

            # Else we just overwrite the team
            team.is_national = response['is_national']
            team.name = response['name']
            team.country = response['country']
            team.founded = response['founded']
            team.venue_name = response['venue_name']
            team.venue_id = response['venue_id']
            team.venue_surface = response['venue_surface']
            team.venue_address = response['venue_address']
            team.venue_city = response['venue_city']
            team.venue_capacity = response['venue_capacity']
            team.coach_name = response['coach_name']
            team.coach_id = response['coach_id']

            for competition_id in response['leagues'].split(","):
                # In what competitions does this team belong?
                competition = get_competition(external_id=competition_id)
                # Does the competition actually exist?
                if competition:
                    team.competitions.append(competition)

            merge(team)
            persist(team)
