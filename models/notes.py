from datetime import datetime
import peewee as orm

from connectors.sqlite import db_sqlite
from models.users import User


class Note(orm.Model):
    author = orm.ForeignKeyField(User)
    title = orm.CharField(max_length=160)
    body = orm.TextField()
    created_at = orm.DateTimeField()
    edited_at = orm.DateTimeField()

    class Meta:
        database = db_sqlite


