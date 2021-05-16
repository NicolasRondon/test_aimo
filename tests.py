from models.notes import Note
from models.users import User, UserToken
from connectors.sqlite import db_sqlite
import requests
import json
import os


class TestAimoApiBuilder():
    def __init__(self):
        self.base = "http://localhost:8000"
        self.user_data = {
            "username": "user_demo",
            "password": "password_demo"
        }
        self.token = None

    def clean_database(self):
        db_sqlite.connect()
        db_sqlite.drop_tables([User, UserToken, Note])
        db_sqlite.create_tables([User, UserToken, Note])
        db_sqlite.close()
        return

    def test_register(self):
        url = f"{self.base}/api/v1/users"
        user = requests.post(url=url, json=self.user_data)
        user_info = user.json()
        assert self.user_data['username'] == user_info['user']['username']

    def test_login(self):
        url = f"{self.base}/api/v1/users/login"
        user = requests.post(url=url, json=self.user_data)
        assert 'token' in user.json()

    def test_login_incorrect(self):
        url = f"{self.base}/api/v1/users/login"
        false_user = {
            "username": "no user",
            "password": "no password"

        }
        user = requests.post(url=url, json=false_user)
        assert 'error' in user.json()

    def test_refresh_token(self):
        url = f"{self.base}/api/v1/users/login"
        url_refresh = f"{self.base}/api/v1/users/refresh"
        user = requests.post(url=url, json=self.user_data)
        user_data = user.json()
        token = user_data['token']
        refresh_token = requests.post(url=url_refresh, headers={"Authorization": token})
        refresh_token = refresh_token.json()
        self.token = refresh_token['token']
        assert 'token' in refresh_token

    def test_create_note(self):
        url = f"{self.base}/api/v1/notes"
        note_data = {
            "title": "Title demo",
            "body": "Body demo"
        }
        note = requests.post(url=url, json=note_data, headers={"Authorization": self.token})
        note_info = note.json()
        assert note_data['body'] == note_info['body']

    def test_list_note(self):
        url = f"{self.base}/api/v1/notes"
        note = requests.get(url=url, headers={"Authorization": self.token})
        note_info = note.json()
        assert 'title' in note_info[0]


class TestDirector:
    def __init__(self):
        self.builder = None

    def construct_tests(self, builder):
        self.builder = builder
        steps = (
            builder.clean_database,
            builder.test_register,
            builder.test_login,
            builder.test_login_incorrect,
            builder.test_refresh_token,
            builder.test_create_note,
            builder.test_list_note
        )
        [step() for step in steps]


director = TestDirector()
director.construct_tests(TestAimoApiBuilder())
