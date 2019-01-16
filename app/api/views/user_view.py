from flask import request
from flask_restful import Resource
from ..models.user_model import UserModel
from ..schemas.user_schema import UserSchema
from marshmallow import ValidationError


class Register(Resource):
    """ Resource for user registration """

    def post(self):
        """ Endpoint to register new user """

        self.db = UserModel()

        status_code = 200
        message = ''
        response = {}

        data = request.get_json()

        if not data:
            status_code = 400
            message = 'No data provided'

        else:
            try:
                data = UserSchema().load(data)

                if self.db.exists('email', data['email']):
                    status_code = 409
                    message = 'Email already exists'

                elif self.db.exists('email', data['email']):
                    status_code = 409
                    message = 'Email already exists'

                else:
                    self.db.save(data)
                    status_code = 201
                    message = 'User created successfully'

            except ValidationError as error:
                status_code = 400
                message = 'Invalid data provided'

                response.update({'errors': error.messages})

        response.update({'status': status_code, 'message': message})
        return response, status_code
