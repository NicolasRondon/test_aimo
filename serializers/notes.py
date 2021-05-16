from datetime import datetime

from marshmallow import Schema, fields

from serializers.fields import MyDateTimeField
from serializers.users import UserSchema


class NoteSchema(Schema):
    author = fields.Integer(required=True)
    title = fields.Str(required=True)
    body = fields.Str(required=True)
    created_at = MyDateTimeField()
    edited_at = MyDateTimeField()


class NoteEditSchema(Schema):
    title = fields.Str()
    body = fields.Str()
    edited_at = MyDateTimeField()
