import logging

from pyramid.view import view_config

from ..models.tweet import get_tweet, list_tweets
from ..models.match import get_match

log = logging.getLogger(__name__)


@view_config(route_name='tweets.get', permission='public',
             renderer="json")
def tweets_get(request):
    tweet_id = request.matchdict['tweet_id']
    tweet = get_tweet(id_=tweet_id)

    return {
        'tweet': tweet.to_json_detail()
    }


@view_config(route_name='tweets.list', permission='public',
             renderer="json")
def tweets_list(request):
    match_id = request.params.get('match_id')

    tweets = list_tweets()

    if match_id:
        match_tweets = []
        match = get_match(id_=match_id)
        for tweet in tweets:
            if match == tweet.match:
                match_tweets.append(tweet)

        tweets = match_tweets

    return {
        'tweets': [tweet.to_json() for tweet in tweets]
    }
