from datetime import datetime
import peewee as orm

from aimo.bridge import ApiAimoBridge
from connectors.sqlite import db_sqlite
from serializers.users import UserSerializer
from utils import make_password


class User(orm.Model):
    username = orm.CharField(unique=True, max_length=187)
    join_date = orm.DateTimeField(default=datetime.now)
    password = orm.CharField(null=False)

    class Meta:
        database = db_sqlite


class UserToken(orm.Model):
    user = orm.ForeignKeyField(User)
    token = orm.CharField()

    class Meta:
        database = db_sqlite


usuarios = ApiAimoBridge(User)
print(usuarios.last)
user = UserSerializer(many=True).dump(usuarios.all)
print(user)
