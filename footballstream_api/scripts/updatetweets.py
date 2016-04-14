import logging
import os
import sys

from pyramid.paster import (
    get_appsettings,
    setup_logging)
from sqlalchemy import engine_from_config
from twython import Twython

import transaction

from ..models import merge, persist
from ..models.meta import Base, DBSession
from ..models.competition import Competition  # noqa
from ..models.user import User, get_user  # noqa
from ..models.match import Match, get_match, list_matches  # noqa
from ..models.tweet import Tweet, get_tweet  # noqa
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
    update_tweets(settings)
    print("Tweets successfuly updated.")


def update_tweets(settings):
    app_key = settings['twitter-api.app_key']
    # app_secret = settings['twitter-api.app_secret']
    access_token = settings['twitter-api.access_token']
    # access_token_secret = settings['twitter-api.access_token_secret']
    current_matches = list_matches(current=True)

    if not current_matches:
        log.info("No current matches at this time")

    for match in current_matches:
        home_team = None
        away_team = None

        if match.localteam_name:
            home_team = match.localteam_name
        if match.visitorteam_name:
            away_team = match.visitorteam_name
        if match.localteam and match.localteam.name:
            home_team = match.localteam.name
        if match.visitorteam and match.visitorteam.name:
            away_team = match.visitorteam.name

        if not home_team and not away_team:
            return

        search_query = '#{}{} OR "{}" OR "{}" -RT'\
            .format(home_team[:3],
                    away_team[:3],
                    home_team,
                    away_team)\
            .upper()

        twitter = Twython(app_key, access_token=access_token)
        twitter_result = twitter.search(q=search_query,
                                        result_type='recent',
                                        count=500
                                        )

        if not twitter_result['statuses']:
            return

        with transaction.manager:
            for obj in twitter_result['statuses']:
                # Does the tweet exist yet?
                tweet = get_tweet(text=obj['text'])

                # To what match does this tweet belong?
                tweet_match = get_match(id_=match.id)

                # If commentary doesn't exist yet, we create a new one
                if not tweet:
                    log.info('Tweet does not yet exist,'
                             'creating tweet')
                    log.info(obj['text'])
                    log.info(obj['user']['screen_name'])
                    tweet = Tweet()
                    tweet.external_id = obj['id']

                # Else we just overwrite the tweet
                tweet.retweet_count = obj['retweet_count']
                tweet.favorite_count = obj['favorite_count']
                tweet.lang = obj['lang']
                tweet.text = obj['text']
                tweet.created_at = obj['created_at']
                tweet.screen_name = obj['user']['screen_name']
                tweet.name = obj['user']['name']
                tweet.profile_image_url = obj['user']['profile_image_url']\
                    .replace("_normal", "")
                tweet.description = obj['user']['description']
                tweet.followers_count = obj['user']['followers_count']

                tweet.match = tweet_match
                merge(tweet)
                persist(tweet)

        rate_limit = twitter.get_lastfunction_header('x-rate-limit-remaining')
        log.info("{} Start of log: '{}' {}".format("-" * 40, "rate_limit",
                                                   "-" * 40))
        log.info(rate_limit)
        log.info("{} End of log: '{}' {}".format("-" * 40, "rate_limit",
                                                 "-" * 40))
