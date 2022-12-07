from marshmallow import Schema, fields


class SoundSchema(Schema):
    value = fields.Integer(required=True)
    sensorId = fields.String(required=True)

