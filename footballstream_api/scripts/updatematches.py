import datetime
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
from ..models.match import Match, get_match  # noqa
from ..models.team import Team, get_team  # noqa

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
    update_matches(settings)
    print('Matches successfully updated')


def update_matches(settings):
    api_key = settings['football-api.key']
    api_url = settings['football-api.url']

    log.info("Getting info for upcoming matches")
    api_endpoint = "/matches"

    # Get date of 7 days from now
    d = datetime.datetime.now()
    d += datetime.timedelta(14)
    next_week = d.strftime("%d.%m.%Y")
    d = datetime.datetime.now()
    d += datetime.timedelta(-14)
    last_week = d.strftime("%d.%m.%Y")

    # Get matches from today to next week days from now
    payload = {'from_date': last_week,
               'to_date': next_week,
               'Authorization': api_key}
    request = requests.get(api_url + api_endpoint, params=payload)
    response = request.json()

    # Check if this object actually has matches or is
    # a faux object
    if request.status_code != 200:
        return

    for obj in response:
        with transaction.manager:
            # Does the match exist yet?
            match = get_match(external_id=obj['id'])

            # If not, we create a new match
            if not match:
                log.info("Match does not yet exist, creating match")
                match = Match()
                match.external_id = obj['id']

            # Else we just overwrite the match
            match.season = obj['season']
            match.week = obj['week'] if obj['week'] else None
            match.venue = obj['venue']
            match.venue_id = obj['venue_id'] if obj['venue_id'] else None
            match.venue_city = obj['venue_city']
            match.status = obj['status']
            match.timer = obj['timer']
            match.localteam_name = obj['localteam_name']
            if obj['localteam_score'] and obj['localteam_score'] != '?':
                match.localteam_score = obj['localteam_score']
            match.visitorteam_name = obj['visitorteam_name']
            if obj['visitorteam_score'] and obj['visitorteam_score'] != '?':
                match.visitorteam_score = obj['visitorteam_score']
            match.ht_score = obj['ht_score']
            match.ft_score = obj['ft_score']
            match.et_score = obj['et_score']
            match.penalty_local = obj['penalty_local']
            match.penalty_visitor = obj['penalty_visitor']

            # Format the date
            try:
                string_time = "{} {}".format(obj['formatted_date'],
                                             obj['time'])
                time_obj = datetime.datetime.strptime(string_time,
                                                      "%d.%m.%Y %H:%M") + datetime.timedelta(hours=2)
                match.date_start = time_obj
            except:
                log.info("This match does not have a startdate")

            # Create relations
            competition = get_competition(external_id=obj['comp_id'])
            localteam = get_team(external_id=obj['localteam_id'])
            visitorteam = get_team(external_id=obj['visitorteam_id'])
            match.competition = competition
            match.localteam = localteam
            match.visitorteam = visitorteam

            merge(match)
            # persist(match)
