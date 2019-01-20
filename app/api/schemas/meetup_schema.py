from marshmallow import Schema, fields
from ..utils.validator import required, date, tags


class MeetupSchema(Schema):
    """ Schema for Meetups """

    id = fields.Int(dump_only=True)
    topic = fields.Str(required=True, validate=(required))
    description = fields.Str(required=True, validate=(required))
    location = fields.Str(required=True, validate=(required))
    happening_on = fields.Str(required=True, validate=(required, date))
    tags = fields.List(fields.Str(), required=True, validate=(tags),
                       error_messages={'required': 'No meetup tags provided'})
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    attendees = fields.Int(dump_only=True)
