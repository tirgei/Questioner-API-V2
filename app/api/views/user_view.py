from flask import request
from flask_restful import Resource
from ..models.user_model import UserModel
from ..schemas.user_schema import UserSchema
from marshmallow import ValidationError
from app.api.models.token_model import RevokedTokenModel
from datetime import timedelta
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

        try:
            signup_data = request.get_json()

            if not signup_data:
                status_code = 400
                message = 'No data provided in the request'

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

                        status_code = 201
                        message = 'User created successfully'
                        response.update({
                            'data': result
                        })

                except ValidationError as error:
                    status_code = 422
                    message = 'Invalid data provided in the request'

                    response.update({'errors': error.messages})

        except:
            status_code = 400
            message = 'No data provided in the request'

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

        try:
            login_data = request.get_json()

            if not login_data:
                message = 'No data provided in the request'
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
                                status_code = 400
                                message = 'Incorrect password'

                            else:
                                access_token = create_access_token(
                                    identity=user['id'])
                                refresh_token = create_refresh_token(
                                    identity=True,
                                    expires_delta=timedelta(days=365))

                                status_code = 200
                                message = 'User logged in successfully'
                                response.update({
                                    'access_token': access_token,
                                    'refresh_token': refresh_token,
                                    'user_id': user['id']
                                })

                    except:
                        status_code = 400
                        message = 'Invalid credentials provided'

                except ValidationError as error:
                    errors = error.messages

                    status_code = 422
                    message = 'Invalid data provided in the request'
                    response.update({'errors': errors})

        except:
            message = 'No data provided in the request'
            status_code = 400

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


class Profile(Resource):
    """ Resource for user profile """

    def __init__(self):
        self.db = UserModel()

    def get(self, user_id):
        """ Endpoint to fetch user profile """

        status_code = 200
        response = {}

        if not self.db.exists('id', user_id):
            status_code = 404
            response.update({'message': 'User not found'})
        else:
            user = self.db.find(user_id)
            result = UserSchema().dump(user)

            status_code = 200
            response.update({'data': result})

        response.update({'status': status_code})
        return response, status_code
