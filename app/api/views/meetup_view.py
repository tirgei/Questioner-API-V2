from flask import request
from ..schemas.meetup_schema import MeetupSchema
from ..schemas.rsvp_schema import RsvpSchema
from ..models.meetup_model import MeetupModel
from ..models.rsvp_model import RsvpModel
from ..models.user_model import UserModel
from marshmallow import ValidationError
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from flask_restful import Resource


class Meetups(Resource):
    """ Resource for meetup endpoints """

    def __init__(self):
        self.db = MeetupModel()
        self.user_db = UserModel()

    @jwt_required
    def post(self):
        """ Endpoint to create meetup """

        message = ''
        status_code = 200
        response = {}

        current_user = get_jwt_identity()

        if not self.user_db.is_admin(current_user):
            message = 'Not authorized'
            status_code = 401

        else:
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
                    response.update({'data': result})

                except ValidationError as err:
                    errors = err.messages

                    status_code = 400
                    message = 'Invalid data provided'
                    response.update({'errors': errors})

        response.update({'status': status_code, 'message': message})
        return response, status_code

    def get(self):
        """ Endpoint to fetch all meetups """

        meetups = self.db.all()
        result = MeetupSchema(many=True).dump(meetups)
        return {'status': 200, 'data': result}, 200


class Meetup(Resource):
    """ Resource for single meetup """

    def __init__(self):
        self.db = MeetupModel()
        self.user_db = UserModel()

    def get(self, meetup_id):
        """ Endpoint to fetch specific meetup """

        status_code = 200
        response = {}

        if not self.db.exists('id', meetup_id):
            status_code = 404
            response.update({'message': 'Meetup not found'})

        else:
            meetup = self.db.find(meetup_id)
            result = MeetupSchema().dump(meetup)

            status_code = 200
            response.update({'data': result})

        response.update({'status': status_code})
        return response, status_code

    @jwt_required
    def delete(self, meetup_id):
        """ Endpoint to delete meetup """

        message = ''
        status_code = 200
        response = {}

        current_user = get_jwt_identity()

        if not self.user_db.is_admin(current_user):
            message = 'Not authorized'
            status_code = 401

        else:
            if not self.db.exists('id', meetup_id):
                status_code = 404
                message = 'Meetup not found'

            else:
                self.db.delete(meetup_id)

                status_code = 200
                message = 'Meetup deleted successfully'

        response.update({'status': status_code, 'message': message})
        return response, status_code


class MeetupRsvp(Resource):
    """ Resource for meetup rsvp """

    def __init__(self):
        self.db = RsvpModel()
        self.meetup_db = MeetupModel()

    @jwt_required
    def post(self, meetup_id, rsvp):
        """ Endpoint to RSVP to meetup """

        message = ''
        status_code = 200
        response = {}

        valid_responses = ('yes', 'no', 'maybe')

        current_user = get_jwt_identity()

        if not self.meetup_db.exists('id', meetup_id):
            status_code = 404
            message = 'Meetup not found'

        elif rsvp not in valid_responses:
            status_code = 400
            message = 'Invalid rsvp'

        elif self.db.exists(meetup_id, current_user):
            status_code = 403
            message = 'Meetup already responded'

        else:
            rsvp_data = {
                'meetup_id': meetup_id,
                'user_id': current_user,
                'response': rsvp
            }

            res = self.db.save(rsvp_data)
            status_code = 200
            message = 'Meetup rsvp successfully'
            result = RsvpSchema().dump(res)
            response.update({'data': result})

        response.update({'status': status_code, 'message': message})
        return response, status_code
