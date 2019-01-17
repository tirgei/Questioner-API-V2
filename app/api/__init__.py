from flask_restful import Api
from flask import Blueprint
from .views.user_view import Register, Login, RefreshToken
from .views.meetup_view import Meetups

v2 = Blueprint('version_2', __name__, url_prefix='/api/v2')

api = Api(v2)

api.add_resource(Register, '/auth/signup')
api.add_resource(Login, '/auth/login')
api.add_resource(RefreshToken, '/refresh-token')
api.add_resource(Meetups, '/meetups')
