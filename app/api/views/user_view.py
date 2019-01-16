from flask import request
from flask_restful import Resource
from ..models.user_model import UserModel
from ..schemas.user_schema import UserSchema
from marshmallow import ValidationError
from flask_jwt_extended import (create_access_token, create_refresh_token)


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

                elif self.db.exists('username', data['username']):
                    status_code = 409
                    message = 'Username already exists'

                else:
                    user = self.db.save(data)
                    result = UserSchema(exclude=['password']).dump(user)
                    access_token = create_access_token(identity=user['id'])
                    refresh_token = create_refresh_token(identity=user['id'])

                    status_code = 201
                    message = 'User created successfully'
                    response.update({
                        'data': result,
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    })

            except ValidationError as error:
                status_code = 400
                message = 'Invalid data provided'

                response.update({'errors': error.messages})

        response.update({'status': status_code, 'message': message})
        return response, status_code
