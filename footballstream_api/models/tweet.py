# encoding: utf-8
import logging
import time

from sqlalchemy import (BigInteger, Column, DateTime, ForeignKey, Integer,
                        String, desc)
from sqlalchemy.orm import relationship

from .meta import Base, DBSession

log = logging.getLogger(__name__)


class Tweet(Base):
    __tablename__ = "tweet"

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('match.external_id'))
    match = relationship('Match', backref='tweets')
    # Tweet
    external_id = Column(BigInteger, unique=True)
    retweet_count = Column(Integer)
    favorite_count = Column(Integer)
    lang = Column(String)
    text = Column(String)
    created_at = Column(String)
    # User
    screen_name = Column(String)
    name = Column(String)
    profile_image_url = Column(String)
    description = Column(String)
    followers_count = Column(Integer)
    date_created = Column(DateTime, default=time.ctime())

    def __json__(self):
        # set fields here
        fields = ("id",
                  "match_id",
                  "external_id",
                  "retweet_count",
                  "favorite_count",
                  "lang",
                  "text",
                  "created_at",
                  "screen_name",
                  "name",
                  "profile_image_url",
                  "description",
                  "followers_count"
                  )

        retval = dict((k, getattr(self, k, None)) for k in fields)
        # extra fields below
        if self.match:
            retval['match'] = self.match.to_json()
        return retval

    def to_json(self):
        return self.__json__()


def get_tweet(id_=None, external_id=None, text=None):
    q = DBSession.query(Tweet)
    if id_:
        q = q.filter(Tweet.id == id_)
    if external_id:
        q = q.filter(Tweet.external_id == external_id)
    if text:
        q = q.filter(Tweet.text == text)
    return q.first()


def list_tweets():
    q = DBSession.query(Tweet)
    q = q.order_by(desc(Tweet.date_created)).limit(100)
    return q.all()
