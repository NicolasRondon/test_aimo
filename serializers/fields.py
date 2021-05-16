from datetime import datetime

from marshmallow import fields


class MyDateTimeField(fields.DateTime):
    def _deserialize(self, value, attr, data):
        if isinstance(value, datetime):
            return value
        return super()._deserialize(value, attr, data)
