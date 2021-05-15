from marshmallow import Schema, fields, validate


class UserSerializer(Schema):
    username = fields.Str()
    password = fields.Str(required = True,
                          validate=[validate.Length(min=8,max=15)])
    join_date = fields.DateTime()

# user = User(name="Monty", email="monty@python.org")
# schema = UserSchema()
# result = schema.dump(user)