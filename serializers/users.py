from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True,
                          validate=[validate.Length(min=8, max=15)],
                          load_only=True)
    join_date = fields.DateTime(required=False)


class UserTokenSchema(Schema):
    user = fields.Nested(UserSchema)
    token = fields.String()
    date_expirated = fields.DateTime()
