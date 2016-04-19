import logging
import json
import os
import sys
import time

from pyramid.paster import (
    get_appsettings,
    setup_logging)

import requests

from sqlalchemy import engine_from_config

import transaction

from ..models import merge, persist
from ..models.meta import Base, DBSession
from ..models.competition import Competition, get_competition  # noqa
from ..models.commentary import Commentary, get_commentary  # noqa
from ..models.event import Event, get_event  # noqa
from ..models.match import Match, get_match, list_matches  # noqa
from ..models.team import Team  # noqa

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
    update_commentaries(settings)
    print('Live matches successfully updated')


def update_commentaries(settings):
    api_key = settings['football-api.key']
    api_url = settings['football-api.url']
    log.info("{} {} {}".format("-" * 40, time.strftime("%H:%M:%S %d-%m-%Y"), "-" * 40))

    current_matches = list_matches(current=True)
    if not current_matches:
        log.info("No current matches at this time")
    for match in current_matches:
        log.info("{} Start of match update for '{}' {}".format("-" * 40, match.id, "-" * 40))
        log.info('Getting live commentaries for match with id: {}'
                 .format(match.external_id))
        api_endpoint = "/commentaries/{}".format(match.external_id)

        payload = {'Authorization': api_key}
        request = requests.get(api_url + api_endpoint, params=payload)
        response = request.json()

        # Check if this object actually has a team or is
        # a faux object
        if request.status_code == 200:
            comments = response['comments']
            if comments:
                with transaction.manager:
                    obj = comments[1]
                    # Is there already a commentary for this match?
                    commentary = get_commentary(match_id=match.external_id)

                    # To what match does this event belong?
                    com_match = get_match(id_=match.id)

                    # If commentary doesn't exist yet, we create a new one
                    if not commentary:
                        log.info('Commentary does not yet exist,'
                                 'creating commentary')
                        log.info(obj['comment'])
                        log.info(obj['minute'])
                        commentary = Commentary()
                        commentary.external_id = obj['id']

                    # Else we just overwrite the commentary
                    commentary.isgoal = obj['isgoal']
                    commentary.comment = obj['comment']
                    commentary.minute = obj['minute']
                    commentary.important = obj['important']
                    commentary.match = com_match

                    merge(commentary)
                    persist(commentary)

                    merge_match = get_match(id_=match.id)
                    merge_match.lineup = json.dumps(response['lineup'])
                    merge_match.playerstats = json.dumps(response['player_stats'])
                    merge_match.subs = json.dumps(response['subs'])
                    merge_match.match_stats = json.dumps(response['match_stats'])
                    merge_match.match_info = json.dumps(response['match_info'])
                    merge(merge_match)
                    persist(merge_match)

        log.info('Getting live events for match with id: {}'
                 .format(match.external_id))
        api_endpoint = "/matches/{}".format(match.external_id)

        payload = {'Authorization': api_key}
        request = requests.get(api_url + api_endpoint, params=payload)
        response = request.json()

        # Check if this object actually has a team or is
        # a faux object
        if request.status_code == 200:
            events = response['events']
            if events:
                for obj in events:
                    with transaction.manager:
                        # Does the event exist yet?
                        event = get_event(external_id=obj['id'])

                        # To what match does this event belong?
                        match = get_match(id_=match.id)

                        # To what team does this event belong
                        team = None
                        if obj['team'] == "localteam":
                            team = match.localteam
                        elif obj['team'] == "visitorteam":
                            team = match.visitorteam

                        # If event doesn't exist yet, we create a new one
                        if not event:
                            log.info("Event does not yet exist, creating event")
                            log.info(obj['type'])
                            log.info(obj['player'])
                            event = Event()
                            event.external_id = obj['id']

                        # Else we just overwrite the event
                        event.type = obj['type']
                        event.minute = obj['minute']
                        if obj['extra_min']:
                            event.extra_min = obj['extra_min']
                        event.player = obj['player']
                        event.assist = obj['assist']
                        event.result = obj['result']
                        event.match = match
                        event.team = team

                        merge(event)
                        persist(event)
    log.info("{}".format("-" * 100))
