from marshmallow import Schema, fields
from ..utils.validator import required


class CommentSchema(Schema):
    """ Schema for Comments """

    id = fields.Int(dump_only=True)
    body = fields.Str(required=True, validate=(required))
    user_id = fields.Int(dump_only=True)
    question_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)