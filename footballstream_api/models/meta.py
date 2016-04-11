from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (scoped_session, sessionmaker)
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Executable, ClauseElement

from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension(),
                                        expire_on_commit=False))
Base = declarative_base()


class CreateView(Executable, ClauseElement):
    def __init__(self, name, select):
        self.name = name
        self.select = select


@compiles(CreateView)
def visit_create_view(element, compiler, **kw):
    return "CREATE VIEW %s AS %s" % \
        (element.name, compiler.process(element.select, literal_binds=True))
