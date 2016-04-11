# encoding: utf-8
import logging
import random

from sqlalchemy import (Column, Integer, String)
from .meta import DBSession, Base

log = logging.getLogger(__name__)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)

    def __json__(self):
        # set fields here
        fields = ("id",
                  "firstname",
                  "lastname",
                  "email"
                  )

        retval = dict((k, getattr(self, k, None)) for k in fields)
        # extra fields below
        # retval['extra_field'] = "something extra"
        return retval

    def to_json(self):
        return self.__json__()


def get_user(id_=None):
    q = DBSession.query(User)
    if id_:
        q = q.filter(User.id == id_)
    return q.first()


def list_users():
    q = DBSession.query(User)
    return q.all()
