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
            message = 'No data provided'
            status_code = 400

        else:
            try:
                data = CommentSchema().load(comment_data)

                data['user_id'] = get_jwt_identity()
                data['question_id'] = question_id
                comment = self.db.save(data)
                result = CommentSchema().dump(comment)

                status_code = 201
                message = 'Comment posted successfully'
                response.update({'data': result})

            except ValidationError as err:
                errors = err.messages

                status_code = 400
                message = 'Invalid data provided'
                response.update({'errors': errors})

        response.update({'status': status_code, 'message': message})
        return response, status_code
