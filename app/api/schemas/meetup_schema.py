from marshmallow import Schema, fields, post_load, pre_dump
from ..utils.validator import required, date, tags
from datetime import datetime


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

    @post_load
    def db_date(self, data):
        """ Function to format date to yyyy-mm-dd """
        formatted_date = datetime.strptime(data['happening_on'], "%d/%m/%Y")

        data['happening_on'] = formatted_date.strftime("%Y-%m-%d")
        return data

    @pre_dump
    def response_data(self, data):
        """ Function to format date to dd/mm/yyyy """
        formatted_date = datetime.strptime(data['happening_on'], "%Y-%m-%d")

        data['happening_on'] = formatted_date.strftime("%d/%m/%Y")
        return data
