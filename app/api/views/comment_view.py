from flask import request
from ..schemas.comment_schema import CommentSchema
from ..models.comment_model import CommentModel
from ..models.question_model import QuestionModel
from marshmallow import ValidationError
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from flask_restful import Resource


class Comment(Resource):
    """ Resource for comments endpoints """

    def __init__(self):
        self.db = CommentModel()
        self.question_db = QuestionModel()

    @jwt_required
    def post(self, question_id):
        """ Endpoint to post comment to meetup question """

        message = ''
        status_code = 200
        response = {}

        comment_data = request.get_json()

        if not self.question_db.exists('id', question_id):
            message = 'Question not found'
            status_code = 404

        elif not comment_data:
            message = 'No data provided in the request'
            status_code = 400

        else:
            try:
                data = CommentSchema().load(comment_data)

                if self.db.check_duplicate(question_id, data['body']):
                    message = 'Comment has been posted already'
                    status_code = 409

                else:
                    data['user_id'] = get_jwt_identity()
                    data['question_id'] = question_id
                    comment = self.db.save(data)
                    result = CommentSchema().dump(comment)

                    status_code = 201
                    message = 'Comment posted successfully'
                    response.update({'data': result})

            except ValidationError as err:
                errors = err.messages

                status_code = 422
                message = 'Invalid data provided'
                response.update({'errors': errors})

        response.update({'status': status_code, 'message': message})
        return response, status_code

    def get(self, question_id):
        """ Endpoint to fetch all comments for a question """

        status_code = 200
        response = {}

        if not self.question_db.exists('id', question_id):
            status_code = 404
            response.update({'message': 'Question not found'})

        else:
            comments = self.db.all(question_id)
            result = CommentSchema(many=True).dump(comments)

            status_code = 200
            response.update({'data': result})

        response.update({'status': status_code})
        return response, status_code
