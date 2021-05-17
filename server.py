from datetime import datetime, timedelta

from bottle import Bottle, run, route, request, hook, response, post, put, get
from jwt import DecodeError
from peewee import IntegrityError, DoesNotExist

from aimo.auth import ApiAimoAuth, create_token
from aimo.bridge import ApiAimoBridge
from connectors.sqlite import db_sqlite
from models.notes import Note
from models.users import User, UserToken
from serializers.notes import NoteSchema,  GetNoteSchema
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
                try:
                    user = User.get(User.username == username)
                except DoesNotExist:
                    return {"error": "The credentials are not valid"}
                user_id = user._data['id']
                user_pasword = user._data['password']
                is_password_correct = check_password(password_raw, user_pasword)
                date_exp = datetime.now() + timedelta(hours=9)
                if is_password_correct:
                    try:
                        user_token = UserToken.get(UserToken.user_id == user_id)
                        data_token = user_token._data
                        auth.get_jwt = {
                            "exp": data_token['date_expirated'],
                            "token": data_token['token']
                        }
                        data_response = {"token": auth.token}
                        return data_response
                    except DoesNotExist:
                        user_token = ApiAimoBridge(UserToken)
                        token = create_token(id_item=user_id, auth=auth, model=user_token, exp=date_exp)
                        data_response = {"token": token}
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


@post('/api/v1/users/refresh')
def refresh_token():
    try:
        headers = request.headers['Authorization']
    except KeyError:
        response.status = 400
        return {"error": "Authorization not in headers"}
    try:
        auth = ApiAimoAuth()
        data = auth.decode_jwt(headers, refresh=True)
        try:
            user_token = ApiAimoBridge(UserToken)
            date_exp = datetime.now() + timedelta(hours=9)
            token_info = UserToken.get(UserToken.token == data['token'])
            user_id = token_info._data['user']
            try:
                query = UserToken.delete().where(UserToken.user == user_id)
                print(query)
                query.execute()
            except Exception as e:
                raise e
            token = create_token(id_item=token_info._data['user'], auth=auth, model=user_token, exp=date_exp)
            data_response = {"token": token}
            return data_response
        except DoesNotExist:
            response.status = 400
            return {"error": "Invalid Token"}


    except Exception as e:
        raise e


@post('/api/v1/notes')
def create_notes():
    try:
        headers = request.headers['Authorization']
    except KeyError:
        response.status = 400
        return {"error": "Authorization not in headers"}

    auth = ApiAimoAuth()
    user_id = auth.check_token(UserToken)
    if type(user_id) != int and 'error' in user_id:
        response.status = 400
        return user_id
    print(user_id)
    data = request.json
    if not data:
        response.status = 400
        return {"error": "Body is empty"}
    data['author'] = user_id
    data['created_at'] = datetime.now()
    serializer = NoteSchema().load(data)

    if serializer.errors:
        response.status = 400
        return {"error": serializer.errors}

    note = ApiAimoBridge(Note)
    try:
        new_note = note.create(serializer.data)

        response_data = NoteSchema(only=("id", "title", "body", "created_at")).dump(new_note)
        return response_data.data
    except Exception as e:
        print(51591)
        raise e

@get('/api/v1/notes')
def list_notes():
    try:
        headers = request.headers['Authorization']
    except KeyError:
        response.status = 400
        return {"error": "Authorization not in headers"}

    auth = ApiAimoAuth()
    user_id = auth.check_token(UserToken)
    if type(user_id) != int and 'error' in user_id:
        response.status = 400
        return user_id

    notes = ApiAimoBridge(Note)
    notes_list =notes.wheres((Note.author == user_id))
    serializer = GetNoteSchema(many=True).dump(notes_list)
    if serializer.errors:
        response.status = 400
        return {"error": serializer.errors}
    return {"notes":serializer.data}


run(host='localhost', port=8000)
