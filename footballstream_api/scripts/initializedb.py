import logging
import os
import sys

from pyramid.paster import (
    get_appsettings,
    setup_logging)
from sqlalchemy import engine_from_config

import transaction

from ..models import persist
from ..models.meta import Base, DBSession
from ..models.user import User, get_user  # noqa
from ..models.competition import Competition  # noqa
from ..models.standing import Standing  # noqa
from ..models.match import Match  # noqa
from ..models.commentary import Commentary  # noqa
from ..models.team import Team  # noqa
from ..models.player import Player  # noqa

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
    create_user()
    print("Database initialisation completed.")


def create_user():
    with transaction.manager:
        u = get_user(id_=1)
        if not u:
            u = User()
            u.firstname = "Jordi"
            u.lastname = "Been"
            u.email = "hello@jordibeen.nl"
            persist(u)
