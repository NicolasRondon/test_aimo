from datetime import datetime
import peewee as orm

from connectors.sqlite import db_sqlite


class User(orm.Model):
    username = orm.CharField(unique=True, max_length=187)
    join_date = orm.DateTimeField(default=datetime.now)
    password = orm.CharField(null=False)

    class Meta:
        database = db_sqlite


class UserToken(orm.Model):
    user = orm.ForeignKeyField(User)
    token = orm.CharField()
    date_expirated = orm.DateTimeField()

    class Meta:
        database = db_sqlite
