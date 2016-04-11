import logging
import os
import sys

from pyramid.paster import (
    get_appsettings,
    setup_logging)

import requests

from sqlalchemy import engine_from_config

import transaction

from ..models import persist
from ..models.meta import Base, DBSession
from ..models.competition import Competition, get_competition  # noqa

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
    update_competitions(settings)
    print('Competitions successfully updated')


def update_competitions(settings):
    api_key = settings['football-api.key']
    api_url = settings['football-api.url']
    api_endpoint = "/competitions"

    payload = {'Authorization': api_key}
    request = requests.get(api_url + api_endpoint, params=payload)
    response = request.json()

    with transaction.manager:
        for obj in response:
            competition = get_competition(external_id=obj['id'])
            if not competition:
                competition = Competition()
                competition.external_id = obj['id']
                competition.name = obj['name']
                competition.region = obj['region']
                competition.logo = obj['region']
                persist(competition)
