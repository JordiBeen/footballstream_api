# encoding: utf-8
import logging

from sqlalchemy import (Column, ForeignKey, Integer, String, Table)
from sqlalchemy.orm import relationship

from .meta import Base, DBSession

log = logging.getLogger(__name__)


team_competition = Table(
    'team_competition',
    Base.metadata,
    Column('team_external_id', Integer, ForeignKey('team.external_id')),
    Column('competition_external_id', Integer, ForeignKey('competition.'
                                                          'external_id'))
)


class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, unique=True)
    competitions = relationship('Competition', secondary=team_competition,
                                backref='teams')
    is_national = Column(String)
    name = Column(String)
    country = Column(String)
    founded = Column(String)
    venue_name = Column(String)
    venue_id = Column(Integer)
    venue_surface = Column(String)
    venue_address = Column(String)
    venue_city = Column(String)
    venue_capacity = Column(Integer)
    coach_name = Column(String)
    coach_id = Column(String)

    def __json__(self):
        # set fields here
        fields = ("id",
                  "external_id",
                  "is_national",
                  "name",
                  "country"
                  )

        retval = dict((k, getattr(self, k, None)) for k in fields)
        # extra fields below
        return retval

    def to_json(self):
        return self.__json__()

    def __json_detail__(self):
        # set fields here
        fields = ("id",
                  "external_id",
                  "is_national",
                  "name",
                  "country",
                  "founded",
                  "venue_name",
                  "venue_id",
                  "venue_surface",
                  "venue_address",
                  "venue_city",
                  "venue_capacity",
                  "coach_name",
                  "coach_id"
                  )

        retval = dict((k, getattr(self, k, None)) for k in fields)
        # extra fields below
        retval['competitions'] = [competition.to_json() for competition in
                                  self.competitions]
        return retval

    def to_json_detail(self):
        return self.__json_detail__()

    def __json_minor__(self):
        # set fields here
        fields = ("id",
                  "name"
                  )

        retval = dict((k, getattr(self, k, None)) for k in fields)
        # extra fields below
        return retval

    def to_json_minor(self):
        return self.__json_minor__()


def get_team(id_=None, external_id=None, name=None):
    q = DBSession.query(Team)
    if id_:
        q = q.filter(Team.id == id_)
    if external_id:
        q = q.filter(Team.external_id == external_id)
    if name:
        q = q.filter(Team.name == name)
    return q.first()


def list_teams():
    q = DBSession.query(Team)
    return q.all()
