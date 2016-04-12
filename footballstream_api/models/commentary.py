# encoding: utf-8
import logging

from sqlalchemy import (Column, ForeignKey, Integer, String)
from sqlalchemy.orm import relationship

from .meta import Base, DBSession

log = logging.getLogger(__name__)


class Commentary(Base):
    __tablename__ = "commentary"

    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, unique=True)
    match_id = Column(Integer, ForeignKey('match.external_id'))
    match = relationship('Match', backref='commentaries')
    isgoal = Column(Integer)
    comment = Column(String)
    minute = Column(String)
    important = Column(Integer)

    def __json__(self):
        # set fields here
        fields = ("id",
                  "external_id",
                  "match_id",
                  "isgoal",
                  "comment",
                  "minute",
                  "important"
                  )

        retval = dict((k, getattr(self, k, None)) for k in fields)
        # extra fields below
        # retval['extra_field'] = "something extra"
        return retval

    def to_json(self):
        return self.__json__()


def get_commentary(id_=None, external_id=None):
    q = DBSession.query(Commentary)
    if id_:
        q = q.filter(Commentary.id == id_)
    if external_id:
        q = q.filter(Commentary.external_id == external_id)
    return q.first()


def list_commentaries():
    q = DBSession.query(Commentary)
    return q.all()
