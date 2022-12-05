from marshmallow import Schema, fields


class SoundSchema(Schema):
    value = fields.Integer(required=True)
class MotionSchema(Schema):
    value = fields.Integer(required=True)

