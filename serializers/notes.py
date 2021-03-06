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


class GetNoteSchema(Schema):
    author = fields.Nested(UserSchema)
    title = fields.Str(required=True)
    body = fields.Str(required=True)
    created_at = MyDateTimeField()
    edited_at = MyDateTimeField()


