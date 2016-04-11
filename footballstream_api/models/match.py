# encoding: utf-8
import datetime
import logging
import time

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String)
from sqlalchemy.orm import relationship

from .meta import Base, DBSession

log = logging.getLogger(__name__)


class Match(Base):
    __tablename__ = "match"

    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, unique=True)
    competition_id = Column(Integer, ForeignKey('competition.external_id'))
    competition = relationship('Competition', backref='matches')
    localteam_id = Column(Integer, ForeignKey('team.external_id'))
    localteam = relationship('Team', foreign_keys=[localteam_id],
                             backref='home_matches')
    visitorteam_id = Column(Integer, ForeignKey('team.external_id'))
    visitorteam = relationship('Team', foreign_keys=[visitorteam_id],
                               backref='away_matches')
    date_start = Column(DateTime)
    season = Column(String)
    week = Column(Integer)
    venue = Column(String)
    venue_id = Column(Integer)
    venue_city = Column(String)
    status = Column(String)
    timer = Column(String)
    localteam_name = Column(String)
    localteam_score = Column(Integer)
    visitorteam_name = Column(String)
    visitorteam_score = Column(Integer)
    ht_score = Column(String)
    ft_score = Column(String)
    et_score = Column(String)
    penalty_local = Column(String)
    penalty_visitor = Column(String)
    date_created = Column(DateTime, default=time.ctime())

    def __json__(self):
        # set fields here
        fields = ("id",
                  "venue"
                  )

        retval = dict((k, getattr(self, k, None)) for k in fields)
        # extra fields below
        if self.localteam and self.visitorteam:
            retval['matchup'] = "{} - {}".format(self.localteam.name,
                                                 self.visitorteam.name)
        retval['competition'] = "{} - {}".format(self.competition.region,
                                                 self.competition.name)
        retval['date_start'] = datetime.datetime.strftime(self.date_start,
                                                          "%d-%m-%Y %H:%M")
        return retval

    def to_json(self):
        return self.__json__()

    def __json_detail__(self):
        # set fields here
        fields = ("id",
                  "venue",
                  )

        retval = dict((k, getattr(self, k, None)) for k in fields)
        # extra fields below
        retval['home_team'] = self.localteam.to_json()
        retval['away_team'] = self.visitorteam.to_json()
        retval['competition'] = self.competition.to_json()
        retval['date_start'] = datetime.datetime.strftime(self.date_start,
                                                          "%d-%m-%Y %H:%M")
        return retval

    def to_json_detail(self):
        return self.__json_detail__()


def get_match(id_=None, external_id=None):
    q = DBSession.query(Match)
    if id_:
        q = q.filter(Match.id == id_)
    if external_id:
        q = q.filter(Match.external_id == external_id)
    return q.first()


def list_matches():
    q = DBSession.query(Match)
    return q.all()
