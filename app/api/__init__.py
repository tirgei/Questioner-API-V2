from flask_restful import Api
from flask import Blueprint
from .views.user_view import Register, Login, RefreshToken
from .views.meetup_view import Meetups, Meetup, MeetupRsvp
from .views.question_view import Question, QuestionList
from .views.comment_view import Comment

v2 = Blueprint('version_2', __name__, url_prefix='/api/v2')

api = Api(v2)

api.add_resource(Register, '/auth/signup')
api.add_resource(Login, '/auth/login')
api.add_resource(RefreshToken, '/refresh-token')
api.add_resource(Meetups, '/meetups')
api.add_resource(Meetup, '/meetups/<int:meetup_id>')
api.add_resource(Question, '/questions')
api.add_resource(QuestionList, '/meetups/<int:meetup_id>/questions')
api.add_resource(Comment, '/questions/<int:question_id>/comments')
api.add_resource(MeetupRsvp, '/meetups/<int:meetup_id>/<string:rsvp>')
