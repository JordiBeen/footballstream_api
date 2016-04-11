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
from ..models.competition import Competition, get_competition, list_competitions  # noqa
from ..models.team import Team, get_team  # noqa
from ..models.standing import Standing, get_standing  # noqa

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
    update_standings(settings)
    print('Standings successfully updated')


def update_standings(settings):
    api_key = settings['football-api.key']
    api_url = settings['football-api.url']

    for competition in list_competitions():
        log.info('Getting standings for competition with id: {}'
                 .format(competition.external_id))
        api_endpoint = "/standings/{}".format(competition.external_id)

        payload = {'Authorization': api_key}
        request = requests.get(api_url + api_endpoint, params=payload)
        response = request.json()

        # Check if this object actually has standings or is
        # a faux object
        if request.status_code != 200:
            continue

        with transaction.manager:
            for obj in response:
                # Get team according to standing object,
                # if one doesn't exist, create empty Team
                team = get_team(external_id=obj['team_id'])
                if not team:
                    log.info("Team with id: {} does not exist, creating team"
                             .format(obj['team_id']))
                    team = Team()
                    team.external_id = obj['team_id']
                    persist(team)

                # Get competition according to standing object
                competition = get_competition(external_id=obj['comp_id'])

                # Does the standing exist yet?
                standing = get_standing(competition_id=obj['comp_id'],
                                        team_id=obj['team_id'])

                # If not, we create a new standing
                if not standing:
                    log.info("Standing does not yet exist, creating standing")
                    standing = Standing()

                # Else we just overwrite the standing
                standing.competition = competition
                standing.team = team
                standing.season = obj['season']
                standing.round = obj['round']
                standing.stage_id = obj['stage_id']
                standing.comp_group = obj['comp_group']
                standing.country = obj['country']
                standing.team_name = obj['team_name']
                standing.status = obj['status']
                standing.recent_form = obj['recent_form']
                standing.position = obj['position']
                standing.overall_gp = obj['overall_gp']
                standing.overall_w = obj['overall_w']
                standing.overall_d = obj['overall_d']
                standing.overall_l = obj['overall_l']
                standing.overall_gs = obj['overall_gs']
                standing.overall_ga = obj['overall_ga']
                standing.home_gp = obj['home_gp']
                standing.home_w = obj['home_w']
                standing.home_d = obj['home_d']
                standing.home_l = obj['home_l']
                standing.home_gs = obj['home_gs']
                standing.home_ga = obj['home_ga']
                standing.away_gp = obj['away_gp']
                standing.away_w = obj['away_w']
                standing.away_d = obj['away_d']
                standing.away_l = obj['away_l']
                standing.away_gs = obj['away_gs']
                standing.away_ga = obj['away_ga']
                standing.gd = obj['gd']
                standing.points = obj['points']
                standing.description = obj['description']
                merge(standing)
                persist(standing)
