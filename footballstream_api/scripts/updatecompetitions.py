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
from ..models.user import User, get_user  # noqa

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


def update_competitions(settings):
    api_key = settings['football-api.key']
    api_url = settings['football-api.url']
    api_entrypoint = "/competitions"

    payload = {'Authorization': api_key}
    r = requests.get(api_url + api_entrypoint, params=payload)
    
    log.info("{} Start of log: '{}' {}".format("-" * 40, "r.json()", "-" * 40))
    log.info(r.json())
    log.info("{} End of log: '{}' {}".format("-" * 40, "r.json()", "-" * 40))
    # with transaction.manager:
    #     u = get_user(id_=1)
    #     if not u:
    #         u = User()
    #         u.firstname = "Jordi"
    #         u.lastname = "Been"
    #         u.email = "hello@jordibeen.nl"
    #         persist(u)
