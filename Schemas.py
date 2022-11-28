from marshmallow import Schema, fields


class SoundSchema(Schema):
    soundAvg = fields.Integer(required=True)

