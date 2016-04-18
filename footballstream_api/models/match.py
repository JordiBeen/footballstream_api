# encoding: utf-8
import datetime
import json
import logging
import time

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String,
                        Text, asc, desc, or_, and_)
from sqlalchemy.orm import relationship

from .meta import Base, DBSession
from ..models.team import get_team

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
    lineup = Column(Text)
    playerstats = Column(Text)
    subs = Column(Text)
    match_stats = Column(Text)
    match_info = Column(Text)
    date_created = Column(DateTime, default=time.ctime())

    def __json__(self):
        # set fields here
        fields = ("id",
                  "venue"
                  )

        retval = dict((k, getattr(self, k, None)) for k in fields)
        # extra fields below
        hometeam = None
        awayteam = None
        if self.localteam and self.visitorteam:
            hometeam = self.localteam
            awayteam = self.visitorteam
        elif self.localteam_name and self.visitorteam_name:
            hometeam = get_team(name=self.localteam_name)
            awayteam = get_team(name=self.visitorteam_name)
        if hometeam and awayteam:
            retval['home_team'] = hometeam.to_json()
            retval['away_team'] = awayteam.to_json()
            retval['matchup'] = "{} - {}".format(hometeam.name,
                                                 awayteam.name)
        elif self.localteam_name and self.visitorteam_name:
            retval['matchup'] = "{} - {}".format(self.localteam_name,
                                                 self.visitorteam_name)
        if self.competition:
            retval['competition'] = "{} - {}".format(self.competition.region,
                                                     self.competition.name)
        if self.date_start:
            retval['date_start'] = datetime.datetime.strftime(self.date_start,
                                                              "%d-%m-%Y %H:%M")
        return retval

    def to_json(self):
        return self.__json__()

    def __json_detail__(self):
        # set fields here
        fields = ("id",
                  "season",
                  "week",
                  "venue",
                  "venue_id",
                  "venue_city",
                  "status",
                  "timer",
                  "localteam_score",
                  "visitorteam_score",
                  "ht_score",
                  "ft_score",
                  "et_score",
                  "penalty_local",
                  "penalty_visitor"
                  )

        retval = dict((k, getattr(self, k, None)) for k in fields)
        # extra fields below
        if self.localteam and self.visitorteam:
            hometeam = self.localteam
            awayteam = self.visitorteam
        elif self.localteam_name and self.visitorteam_name:
            hometeam = get_team(name=self.localteam_name)
            awayteam = get_team(name=self.visitorteam_name)
        if hometeam and awayteam:
            retval['home_team'] = hometeam.to_json()
            retval['away_team'] = awayteam.to_json()
            retval['matchup'] = "{} - {}".format(hometeam.name,
                                                 awayteam.name)
        elif self.localteam_name and self.visitorteam_name:
            retval['matchup'] = "{} - {}".format(self.localteam_name,
                                                 self.visitorteam_name)
        if self.competition:
            retval['competition'] = self.competition.to_json()
        retval['date_start'] = datetime.datetime.strftime(self.date_start,
                                                          "%d-%m-%Y %H:%M")
        if self.lineup:
            retval["lineup"] = json.loads(self.lineup)
        if self.playerstats:
            retval["playerstats"] = json.loads(self.playerstats)
        if self.subs:
            retval["subs"] = json.loads(self.subs)
        if self.match_stats:
            retval["match_stats"] = json.loads(self.match_stats)
        if self.match_info:
            retval["match_info"] = json.loads(self.match_info)
        if self.commentaries:
            commentaries = {}
            for commentary in self.commentaries:
                minute = commentary.minute.replace("'", "").replace("''", "")
                if minute == '':
                    continue
                commentaries[minute] = commentary
            sorted(commentaries)
            retval["commentaries"] = [commentaries[commentary].to_json() for commentary
                                      in commentaries]
        if self.events:
            retval["events"] = [event.to_json() for event in self.events]
        if self.tweets:
            retval["tweets"] = [tweet.to_json() for tweet in self.tweets]
        return retval

    def to_json_detail(self):
        return self.__json_detail__()

    def __json_finished__(self):
        # set fields here
        fields = ("id",
                  "venue",
                  "ft_score",
                  )

        retval = dict((k, getattr(self, k, None)) for k in fields)
        # extra fields below
        if self.localteam and self.visitorteam:
            hometeam = self.localteam
            awayteam = self.visitorteam
        elif self.localteam_name and self.visitorteam_name:
            hometeam = get_team(name=self.localteam_name)
            awayteam = get_team(name=self.visitorteam_name)
        if hometeam and awayteam:
            retval['matchup'] = "{} - {}".format(hometeam.name,
                                                 awayteam.name)
        elif self.localteam_name and self.visitorteam_name:
            retval['matchup'] = "{} - {}".format(self.localteam_name,
                                                 self.visitorteam_name)
        if self.competition:
            retval['competition'] = "{} - {}".format(self.competition.region,
                                                     self.competition.name)
        retval['date_start'] = datetime.datetime.strftime(self.date_start,
                                                          "%d-%m-%Y %H:%M")
        return retval

    def to_json_finished(self):
        return self.__json_finished__()


def get_match(id_=None, external_id=None):
    q = DBSession.query(Match)
    if id_:
        q = q.filter(Match.id == id_)
    if external_id:
        q = q.filter(Match.external_id == external_id)
    return q.first()


def list_matches(upcoming=True, current=None, finished=None):
    q = DBSession.query(Match)
    if upcoming and not current and not finished:
        q = q.filter(or_(Match.date_start >= time.ctime(), and_(Match.date_start <= time.ctime(), and_(Match.status != "FT", Match.status != "Pen."))))\
            .order_by(asc(Match.date_start))
    if current:
        q = q.filter(Match.date_start <= time.ctime())\
            .filter(and_(Match.status != "FT", Match.status != "Pen."))\
            .order_by(asc(Match.date_start))
    if finished:
        q = q.filter(Match.date_start <= time.ctime())\
            .filter(or_(Match.status == "FT", Match.status == "Pen."))\
            .order_by(desc(Match.date_start)).limit(100)
    return q.all()
