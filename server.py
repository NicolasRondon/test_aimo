from datetime import datetime, timedelta

from bottle import Bottle, run, route, request, hook, response, post
from peewee import IntegrityError, DoesNotExist

from aimo.auth import ApiAimoAuth
from aimo.bridge import ApiAimoBridge
from connectors.sqlite import db_sqlite
from models.users import User, UserToken
from serializers.users import UserSchema
from utils import check_password

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


@post('/api/v1/users/login')
def login_user():
    try:
        data = request.json
        serializer = UserSchema().load(data)

        if serializer.errors:
            response.status = 400
            return {"error": serializer.errors}

        try:
            try:
                auth = ApiAimoAuth()
                username = serializer.data['username']
                password_raw = serializer.data['password']
                user = User.get(User.username == username)
                user_id = user.id
                user_pasword = user.password
                is_password_correct = check_password(password_raw, user_pasword)
                date_exp = datetime.now() + timedelta(hours=9)
                if is_password_correct:
                    # TODO creacion del token
                    try:
                        user_token = UserToken(id=user_id).get()
                        data_token = user_token._data
                        auth.get_jwt = {
                            "exp": data_token['date_expirated'],
                            "token": data_token['token']
                        }
                        data_response = {"token": auth.token}
                        return data_response
                    except DoesNotExist:
                        user_token = ApiAimoBridge(UserToken)
                        values_cretate_token = {
                            "user_id": user_id,
                            "token": auth.secret_key,
                            "date_expirated": date_exp
                        }
                        user_token.create(values_cretate_token)
                        auth.get_jwt = {
                            "exp": values_cretate_token["date_expirated"],
                            "token": values_cretate_token["token"]
                        }
                        data_response = {"token": auth.token}
                        return data_response

                else:
                    response.status = 400
                    return {"error": "The credentials are not valid"}

            except Exception as e:
                raise e

        except Exception as e:
            raise e

    except Exception as e:
        raise e


run(host='localhost', port=8000)
