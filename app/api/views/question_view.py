from flask import jsonify, request, make_response
from ..schemas.question_schema import QuestionSchema
from ..models.question_model import QuestionModel
from ..models.meetup_model import MeetupModel
from marshmallow import ValidationError
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from flask_restful import Resource


class Question(Resource):
    """ Resource for question endpoints """

    def __init__(self):
        self.db = QuestionModel()
        self.meetup_db = MeetupModel()

    @jwt_required
    def post(self):
        """ Endpoint to post question """

        message = ''
        status_code = 200
        response = {}

        question_data = request.get_json()

        if not question_data:
            message = 'No data provided'
            status_code = 400

        else:
            try:
                data = QuestionSchema().load(question_data)

                if not self.meetup_db.exists('id', data['meetup_id']):
                    message = 'Meetup not found'
                    status_code = 404

                else:
                    data['user_id'] = get_jwt_identity()
                    question = self.db.save(data)
                    result = QuestionSchema().dump(question)

                    status_code = 201
                    message = 'Question posted successfully'
                    response.update({'data': result})

            except ValidationError as err:
                errors = err.messages

                status_code = 400
                message = 'Invalid data provided'
                response.update({'errors': errors})

        response.update({'status': status_code, 'message': message})
        return response, status_code


class QuestionList(Resource):
    """ Resource for questions list """

    def __init__(self):
        self.db = QuestionModel()
        self.meetup_db = MeetupModel()

    def get(self, meetup_id):
        """ Endpoint to fetch all questions for a specific meetup """

        status_code = 200
        response = {}

        if not self.meetup_db.exists('id', meetup_id):
            status_code = 404
            response.update({'message': 'Meetup not found'})

        else:
            questions = self.db.all(meetup_id)
            result = QuestionSchema(many=True).dump(questions)
            response.update({'data': result})

        response.update({'status': status_code})
        return response, status_code