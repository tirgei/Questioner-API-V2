from flask import request
from flask_restful import Resource
from ..models.user_model import UserModel
from ..schemas.user_schema import UserSchema
from marshmallow import ValidationError
from app.api.models.token_model import RevokedTokenModel
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, get_jwt_identity,
                                jwt_refresh_token_required, get_raw_jwt)


class Register(Resource):
    """ Resource for user registration """

    def __init__(self):
        self.db = UserModel()

    def post(self):
        """ Endpoint for user signup """

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


class Login(Resource):
    """ Resource for user login """

    def __init__(self):
        self.db = UserModel()

    def post(self):
        """ Endpoint for user login """

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
                    pw = data['password']

                    if not self.db.exists('username', username):
                        status_code = 404
                        message = 'User not found'

                    else:
                        user = self.db.where('username', username)

                        if not self.db.checkpassword(user['password'], pw):
                            status_code = 422
                            message = 'Incorrect password'

                        else:
                            access_token = create_access_token(
                                identity=user['id'])
                            refresh_token = create_refresh_token(
                                identity=True)

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


class RefreshToken(Resource):
    """ Resource to refresh access token """

    @jwt_refresh_token_required
    def post(self):
        """ Endpoint to refresh user access token """

        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'status': 200, 'message': 'Token refreshed successfully',
                'access_token': access_token}


class Logout(Resource):
    """ Resource to logout user """

    @jwt_required
    def post(self):
        """ Endpoint to logout user """

        user_jti = get_raw_jwt()['jti']

        RevokedTokenModel().save(user_jti)
        return {'status': 200, 'message': 'Logged out successfully'}, 200
