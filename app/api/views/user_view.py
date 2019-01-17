from flask import request
from flask_restful import Resource
from ..models.user_model import UserModel
from ..schemas.user_schema import UserSchema
from marshmallow import ValidationError
from flask_jwt_extended import (create_access_token, create_refresh_token)


class Register(Resource):
    """ Resource for user registration """

    def post(self):
        """ Endpoint for user signup """

        db = UserModel()

        status_code = 200
        message = ''
        response = {}

        signup_data = request.get_json()

        if not signup_data:
            status_code = 400
            message = 'No data provided'

        else:
            try:
                data = UserSchema().load(signup_data)

                if db.exists('email', data['email']):
                    status_code = 409
                    message = 'Email already exists'

                elif db.exists('username', data['username']):
                    status_code = 409
                    message = 'Username already exists'

                else:
                    user = db.save(data)
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


class Login(Resource):
    """ Resource for user login """

    def post(self):
        """ Endpoint for user login """

        db = UserModel()

        message = ''
        status_code = 200
        response = {}

        login_data = request.get_json()

        if not login_data:
            message = 'No data provided'
            status_code = 400

        else:
            try:
                data = UserSchema().load(login_data, partial=True)

                try:
                    username = data['username']
                    password = data['password']

                    print('chechcked pass')

                    if not db.exists('username', username):
                        print('not found')
                        status_code = 404
                        message = 'User not found'

                    else:
                        print('nice')
                        user = db.where('username', username)

                        if not db.checkpassword(user['password'], password):
                            status_code = 422
                            message = 'Incorrect password'

                        else:
                            access_token = create_access_token(identity=user['id'])
                            refresh_token = create_refresh_token(identity=True)

                            status_code = 200
                            message = 'User logged in successfully'
                            response.update({
                                'access_token': access_token,
                                'refresh_token': refresh_token,
                                'user_id': user['id']
                            })

                except:
                    status_code = 400
                    message = 'Invalid credentials'

            except ValidationError as error:
                errors = error.messages

                status_code = 400
                message = 'Invalid data provided'
                response.update({'errors': errors})

        response.update({'status': status_code, 'message': message})
        return response, status_code
