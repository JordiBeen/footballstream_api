# encoding: utf-8
import logging

from sqlalchemy import (Column, ForeignKey, Integer, String)
from sqlalchemy.orm import relationship

from .meta import Base, DBSession

log = logging.getLogger(__name__)


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, unique=True)
    match_id = Column(Integer, ForeignKey('match.external_id'))
    match = relationship('Match', backref='events')
    type = Column(String)
    minute = Column(Integer)
    extra_min = Column(Integer)
    team = Column(String)
    player = Column(String)
    assist = Column(String)
    result = Column(String)

    def __json__(self):
        # set fields here
        fields = ("id",
                  "type"
                  )

        retval = dict((k, getattr(self, k, None)) for k in fields)
        # extra fields below
        # retval['extra_field'] = "something extra"
        return retval

    def to_json(self):
        return self.__json__()


def get_event(id_=None):
    q = DBSession.query(Event)
    if id_:
        q = q.filter(Event.id == id_)
    return q.first()


def list_events():
    q = DBSession.query(Event)
    return q.all()
