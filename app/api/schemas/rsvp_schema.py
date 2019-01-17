from marshmallow import Schema, fields
from ..utils.validator import required


class RsvpSchema(Schema):
    """Schema for Rsvp """

    id = fields.Integer(required=False)
    response = fields.Str(required=True, validate=(required))
    meetup_id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
