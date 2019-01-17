from marshmallow import Schema, fields
from ..utils.validator import required, date


class MeetupSchema(Schema):
    """ Schema for Meetups """

    id = fields.Int(dump_only=True)
    topic = fields.Str(required=True, validate=(required))
    description = fields.Str(required=True, validate=(required))
    location = fields.Str(required=True, validate=(required))
    happening_on = fields.Str(required=True, validate=(required, date))
    tags = fields.List(fields.Str(), required=False)
    images = fields.List(fields.Str(), required=False)