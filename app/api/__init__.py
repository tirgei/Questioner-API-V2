from flask_restful import Api
from flask import Blueprint
from .views.user_view import Register

v2 = Blueprint('version_2', __name__, url_prefix='/api/v2')

api = Api(v2)

api.add_resource(Register, '/auth/signup')
