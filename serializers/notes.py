from marshmallow import Schema, fields, validate

from serializers.users import UserSchema


class NoteSchema(Schema):
    author = fields.Nested(UserSchema)
    title = fields.Str()
    body = fields.Str()
    created_at = fields.DateTime()
    edited_at = fields.DateTime()

