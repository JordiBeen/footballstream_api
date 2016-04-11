import logging
from .user import User  # noqa

from .meta import DBSession

log = logging.getLogger(__name__)


def commit():
    log.debug("Committing DBSession: %r", DBSession.dirty)
    DBSession.commit()


def persist(obj):
    log.debug("persisting object %r", obj)
    DBSession.add(obj)


def delete(obj):
    log.debug("deleting object %r", obj)
    DBSession.delete(obj)


def merge(obj):
    log.debug("merging %r", obj)
    return DBSession.merge(obj)


def rollback():
    log.debug("Rolling back DBSession: %r", DBSession.dirty)
    return DBSession.rollback()


def flush():
    log.debug("flushing session")
    return DBSession.flush()
