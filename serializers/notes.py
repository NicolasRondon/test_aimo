from datetime import datetime

from marshmallow import Schema, fields

from serializers.fields import MyDateTimeField


class NoteSchema(Schema):
    author = fields.Int()
    title = fields.Str(required=True)
    body = fields.Str(required=True)
    created_at = MyDateTimeField()
    edited_at = MyDateTimeField()

