from flask import jsonify, request, make_response
from ..schemas.meetup_schema import MeetupSchema
from ..models.meetup_model import MeetupModel
from marshmallow import ValidationError
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from flask_restful import Resource


class Meetups(Resource):
    """ Resource for meetup endpoints """

    def __init__(self):
        self.db = MeetupModel()

    @jwt_required
    def post(self):
        """ Endpoint to create meetup """

        message = ''
        status_code = 200
        response = {}

        meetup_data = request.get_json()

        if not meetup_data:
            message = 'No data provided'
            status_code = 400

        else:
            try:
                data = MeetupSchema().load(meetup_data)

                new_meetup = self.db.save(data)
                result = MeetupSchema().dump(new_meetup)

                status_code = 201
                message = 'Meetup created successfully'

            except ValidationError as err:
                errors = err.messages

                status_code = 400
                message = 'Invalid data provided'
                response.update({'errors': errors})

        response.update({'status': status_code, 'message': message})
        return response, status_code
