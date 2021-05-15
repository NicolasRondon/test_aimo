# # Run with "python server.py"
#
# from bottle import run
#
# # Start your code here, good luck (: ...
#
#
#
#
from bottle import Bottle, run, route, request, hook, response, post
from peewee import IntegrityError

from aimo.bridge import ApiAimoBridge
from connectors.sqlite import db_sqlite
from models.users import User
from serializers.users import UserSchema

_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'


@hook('before_request')
def db_connect():
    db_sqlite.connect()


@hook('after_request')
def enable_cors():
    if not db_sqlite.is_closed():
        db_sqlite.close()

    response.headers['Access-Control-Allow-Origin'] = _allow_origin
    response.headers['Access-Control-Allow-Methods'] = _allow_methods
    response.headers['Access-Control-Allow-Headers'] = _allow_headers


app = Bottle()


# from models.users import UserToken


@post('/api/v1/users')
def create_users():
    try:
        data = request.json
        serializer = UserSchema().load(data)

        if serializer.errors:
            response.status = 400
            return {"error": serializer.errors}
        try:
            user = ApiAimoBridge(User)
            new_user = user.create(serializer.data)
            new_user = UserSchema(only=("username",)).dump(new_user)
            return {"user": new_user.data}

        except IntegrityError:
            response.status = 400
            return {"error": "There is User with same username"}
    except Exception as e:
        raise e
    # user = ApiAimoBridge(User)
    # serializer = UserSchema().load({"name": "John", "email": "foo"})
    # new_user = user.create()


run(host='localhost', port=8000)
