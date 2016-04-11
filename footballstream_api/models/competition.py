# encoding: utf-8
import logging

from sqlalchemy import (Column, Integer, String)

from .meta import Base, DBSession

log = logging.getLogger(__name__)


class Competition(Base):
    __tablename__ = "competition"

    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, unique=True)
    name = Column(String)
    region = Column(String)

    def __json__(self):
        # set fields here
        fields = ("id",
                  "external_id",
                  "name",
                  "region"
                  )

        retval = dict((k, getattr(self, k, None)) for k in fields)
        # extra fields below
        # retval['extra_field'] = "something extra"
        return retval

    def to_json(self):
        return self.__json__()


def get_competition(id_=None, external_id=None):
    q = DBSession.query(Competition)
    if id_:
        q = q.filter(Competition.id == id_)
    if external_id:
        q = q.filter(Competition.external_id == external_id)
    return q.first()


def list_competitions():
    q = DBSession.query(Competition)
    return q.all()
