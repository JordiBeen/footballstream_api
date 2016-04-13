import os
import sys

from pyramid.paster import get_appsettings, setup_logging

from sqlalchemy import engine_from_config

from ..models.meta import Base, DBSession
from ..models.user import User, get_user  # noqa
from ..models.competition import Competition  # noqa
from ..models.event import Event  # noqa
from ..models.standing import Standing  # noqa
from ..models.match import Match  # noqa
from ..models.commentary import Commentary  # noqa
from ..models.team import Team  # noqa
from ..models.tweet import Tweet  # noqa


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
    Base.metadata.drop_all(engine)
