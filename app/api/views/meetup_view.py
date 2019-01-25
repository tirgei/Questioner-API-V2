from flask import request
from ..schemas.meetup_schema import MeetupSchema
from ..schemas.rsvp_schema import RsvpSchema
from ..models.meetup_model import MeetupModel
from ..models.rsvp_model import RsvpModel
from ..models.user_model import UserModel
from marshmallow import ValidationError
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from flask_restful import Resource
from ..schemas.user_schema import UserSchema


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
            message = 'Only admin is authorized to perform this operation'
            status_code = 403

        else:

            try:
                meetup_data = request.get_json()

                if not meetup_data:
                    message = 'No data provided in the request'
                    status_code = 400

                else:
                    try:
                        data = MeetupSchema().load(meetup_data)
                        duplicate, msg = self.db.check_if_duplicate(data)

                        if duplicate:
                            status_code = 409
                            message = msg

                        else:
                            new_meetup = self.db.save(data)
                            result = MeetupSchema().dump(new_meetup)

                            status_code = 201
                            message = 'Meetup created successfully'
                            response.update({'data': result})

                    except ValidationError as err:
                        errors = err.messages

                        status_code = 422
                        message = 'Invalid data provided in the request'
                        response.update({'errors': errors})

            except:
                message = 'No data provided in the request'
                status_code = 400

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
        self.rsvp_db = RsvpModel()

    def get(self, meetup_id):
        """ Endpoint to fetch specific meetup """

        status_code = 200
        response = {}

        if not self.db.exists('id', meetup_id):
            status_code = 404
            response.update({'message': 'Meetup not found'})

        else:
            meetup = self.db.find(meetup_id)
            attendees = self.rsvp_db.attendees(meetup_id)
            meetup['attendees'] = attendees

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
            message = 'Only admin user is authorized to delete meetups'
            status_code = 403

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
            message = 'Invalid rsvp. The allowed options are yes, no or maybe'

        elif self.db.exists(meetup_id, current_user):
            status_code = 409
            message = 'Reponse already sent for this meetup' 

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


class UpcomingMeetups(Resource):
    """ Resource for upcoming meetups endpoints """

    def __init__(self):
        self.db = MeetupModel()

    def get(self):
        """ Endpoint to fetch all meetups """

        meetups = self.db.upcoming()
        result = MeetupSchema(many=True).dump(meetups)
        return {'status': 200, 'data': result}, 200


class MeetupAttendees(Resource):
    """ Resource for meetup attendees """

    def __init__(self):
        self.db = MeetupModel()

    def get(self, meetup_id):
        """ Endpoint to fetch all meetup attendees """

        message = ''
        status_code = 200
        response = {}

        if not self.db.exists('id', meetup_id):
            status_code = 404
            message = 'Meetup not found'
            response.update({'message': message})

        else:
            users = self.db.attendees(meetup_id)
            result = UserSchema(many=True).dump(users)

            status_code = 200
            response.update({
                'attendees': len(users),
                'users': result
            })

        response.update({'status': status_code})
        return response, status_code


class MeetupTags(Resource):
    """ Resource for updating meetup tags """

    def __init__(self):
        self.db = MeetupModel()
        self.user_db = UserModel()

    @jwt_required
    def patch(self, meetup_id):
        """ Endpoint to update meetup tags """

        message = ''
        status_code = 200
        response = {}

        current_user = get_jwt_identity()

        if not self.user_db.is_admin(current_user):
            message = 'Only admin user is authorized to update meetups'
            status_code = 403

        else:
            meetup_data = request.get_json()

            if not self.db.exists('id', meetup_id):
                status_code = 404
                message = 'Meetup not found'

            elif not meetup_data:
                message = 'No data provided in the request'
                status_code = 400

            elif 'tags' not in meetup_data:
                message = 'No meetup tags provided in the request'
                status_code = 400

            elif not len(meetup_data['tags']) > 0:
                message = 'You need to pass atleast 1 tag for the meetup'
                status_code = 400

            else:
                meetup = self.db.update_tags(meetup_id, meetup_data['tags'])
                result = MeetupSchema().dump(meetup)

                status_code = 200
                message = 'Meetup tags updated successfully'
                response.update({'data': result})

        response.update({'status': status_code, 'message': message})
        return response, status_code
