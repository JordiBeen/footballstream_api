# encoding: utf-8
import logging

from sqlalchemy import (Column, Integer, String)

from .meta import Base, DBSession

log = logging.getLogger(__name__)


class Player(Base):
    __tablename__ = "player"

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


def get_player(id_=None):
    q = DBSession.query(Player)
    if id_:
        q = q.filter(Player.id == id_)
    return q.first()


def list_players():
    q = DBSession.query(Player)
    return q.all()
