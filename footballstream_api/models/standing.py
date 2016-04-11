# encoding: utf-8
import logging

from sqlalchemy import (Column, ForeignKey, Integer, String)
from sqlalchemy.orm import relationship

from .meta import Base, DBSession

log = logging.getLogger(__name__)


class Standing(Base):
    __tablename__ = "standing"

    id = Column(Integer, primary_key=True)
    competition_id = Column(Integer, ForeignKey('competition.external_id'))
    competition = relationship('Competition', backref='standings')
    team_id = Column(Integer, ForeignKey('team.external_id'))
    team = relationship('Team', backref='standings')
    season = Column(String)
    round = Column(Integer)
    stage_id = Column(Integer)
    comp_group = Column(String)
    country = Column(String)
    team_name = Column(String)
    status = Column(String)
    recent_form = Column(String)
    position = Column(Integer)
    overall_gp = Column(Integer)
    overall_w = Column(Integer)
    overall_d = Column(Integer)
    overall_l = Column(Integer)
    overall_gs = Column(Integer)
    overall_ga = Column(Integer)
    home_gp = Column(Integer)
    home_w = Column(Integer)
    home_d = Column(Integer)
    home_l = Column(Integer)
    home_gs = Column(Integer)
    home_ga = Column(Integer)
    away_gp = Column(Integer)
    away_w = Column(Integer)
    away_d = Column(Integer)
    away_l = Column(Integer)
    away_gs = Column(Integer)
    away_ga = Column(Integer)
    gd = Column(Integer)
    points = Column(Integer)
    description = Column(String)

    def __json__(self):
        # set fields here
        fields = ("id",
                  "name",
                  "competition_id",
                  "team_id",
                  "season",
                  "round",
                  "stage_id",
                  "comp_group",
                  "country",
                  "team_id",
                  "team_name",
                  "status",
                  "recent_form",
                  "position",
                  "overall_gp",
                  "overall_w",
                  "overall_d",
                  "overall_l",
                  "overall_gs",
                  "overall_ga",
                  "home_gp",
                  "home_w",
                  "home_d",
                  "home_l",
                  "home_gs",
                  "home_ga",
                  "away_gp",
                  "away_w",
                  "away_d",
                  "away_l",
                  "away_gs",
                  "away_ga",
                  "gd",
                  "points",
                  "description"
                  )

        retval = dict((k, getattr(self, k, None)) for k in fields)
        # extra fields below
        # retval['extra_field'] = "something extra"
        return retval

    def to_json(self):
        return self.__json__()


def get_standing(id_=None, competition_id=None, team_id=None):
    q = DBSession.query(Standing)
    if id_:
        q = q.filter(Standing.id == id_)
    if competition_id:
        q = q.filter(Standing.competition_id == competition_id)
    if team_id:
        q = q.filter(Standing.team_id == team_id)
    return q.first()


def list_standings():
    q = DBSession.query(Standing)
    return q.all()
