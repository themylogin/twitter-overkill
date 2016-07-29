from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import Column

from twitter_overkill.app import app

__all__ = ["db"]


class NotNullableColumn(Column):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("nullable", False)
        super().__init__(*args, **kwargs)


db = SQLAlchemy(app)
db.Column = NotNullableColumn
db.Model.__repr__ = lambda self: "<%s id=%s>" % (self.__class__.__name__, self.id or "0x%x" % id(self))
