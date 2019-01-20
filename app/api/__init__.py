from flask_restful import Api
from flask import Blueprint
from .views.user_view import Register, Login, RefreshToken, Logout
from .views.question_view import Question, QuestionList
from .views.question_view import QuestionDownvote, QuestionUpvote
from .views.comment_view import Comment
from .views.meetup_view import (Meetups, Meetup, MeetupRsvp, UpcomingMeetups,
                                MeetupAttendees, MeetupTags)

v2 = Blueprint('version_2', __name__, url_prefix='/api/v2')

api = Api(v2)

api.add_resource(Register, '/auth/signup')
api.add_resource(Login, '/auth/login')
api.add_resource(Logout, '/auth/logout')
api.add_resource(RefreshToken, '/refresh-token')
api.add_resource(Meetups, '/meetups')
api.add_resource(UpcomingMeetups, '/meetups/upcoming')
api.add_resource(Meetup, '/meetups/<int:meetup_id>')
api.add_resource(MeetupAttendees, '/meetups/<int:meetup_id>/attendees')
api.add_resource(MeetupTags, '/meetups/<int:meetup_id>/tags')
api.add_resource(Question, '/questions')
api.add_resource(QuestionList, '/meetups/<int:meetup_id>/questions')
api.add_resource(Comment, '/questions/<int:question_id>/comments')
api.add_resource(MeetupRsvp, '/meetups/<int:meetup_id>/<string:rsvp>')
api.add_resource(QuestionUpvote, '/questions/<int:question_id>/upvote')
api.add_resource(QuestionDownvote, '/questions/<int:question_id>/downvote')
