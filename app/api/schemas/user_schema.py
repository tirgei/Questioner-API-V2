from marshmallow import Schema, fields
from ..utils.validator import required, password, phonenumber, name


class UserSchema(Schema):
    """Schema for Users """

    id = fields.Integer(dump_only=True)
    firstname = fields.Str(required=True, validate=(required, name))
    lastname = fields.Str(required=True, validate=(required, name))
    username = fields.Str(required=True, validate=(required, name))
    othername = fields.Str(required=False, validate=(name))
    phonenumber = fields.Str(required=True, validate=(phonenumber))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=(required, password))
    registered = fields.DateTime(dump_only=True)
    questions_asked = fields.Int(dump_only=True)
    questions_commented = fields.Int(dump_only=True)
