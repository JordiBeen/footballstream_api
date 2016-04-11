# encoding: utf-8
import logging

from sqlalchemy import (Column, Integer, String)

from .meta import Base, DBSession

log = logging.getLogger(__name__)


class Commentary(Base):
    __tablename__ = "commentary"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __json__(self):
        # set fields here
        fields = ("id",
                  "name"
                  )

        retval = dict((k, getattr(self, k, None)) for k in fields)
        # extra fields below
        # retval['extra_field'] = "something extra"
        return retval

    def to_json(self):
        return self.__json__()


def get_commentary(id_=None):
    q = DBSession.query(Commentary)
    if id_:
        q = q.filter(Commentary.id == id_)
    return q.first()


def list_commentaries():
    q = DBSession.query(Commentary)
    return q.all()
