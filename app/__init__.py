from flask import Flask, jsonify
from instance.config import app_config
from db.db_config import DatabaseConnection
from app.api import v2
from flask_jwt_extended import (JWTManager)
from app.api.models.token_model import RevokedTokenModel
from flask_cors import CORS


@v2.route('/', methods=['GET'])
@v2.route('/index', methods=['GET'])
def index():
    """ Endpoint for index for v2 """
    return jsonify({
        'status': 200,
        'message': 'Welcome to Questioner'
        }), 200


def create_app(config_name):
    """ Function to initialize Flask app """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.url_map.strict_slashes = False
    CORS(app)

    jwt = JWTManager(app)

    handlers(app, jwt)
    initialize_db(config_name)

    app.register_blueprint(v2)

    return app


def initialize_db(config_name):
    """ Function to initialize db """

    try:
        db = DatabaseConnection()
        db.init_connection(config_name)
        db.create_tables()
        db.seed()

    except Exception as error:
        print('Error initiating DB: {}'.format(str(error)))


def handlers(app, jwt):
    """ Function to initialize error handlers """

    @app.route('/', methods=['GET'])
    @app.route('/index', methods=['GET'])
    def landing_page():
        """ Endpoint for landing page """
        return jsonify({
            'status': 200,
            'message': 'Welcome to Questioner'
            }), 200

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            'status': 404,
            'message': 'Url not found. Check your url and try again'
            }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'status': 500,
            'message': 'Your request could not be processed'
            }), 500

    @jwt.token_in_blacklist_loader
    def check_blacklisted(token):
        jti = token['jti']
        return RevokedTokenModel().is_blacklisted(jti)

    @jwt.expired_token_loader
    def expired_token():
        return jsonify({
            'status': 401,
            'message': 'Token has expired'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token(reason):
        return jsonify({
            'status': 401,
            'message': reason
        }), 401

    @jwt.revoked_token_loader
    def revoked_token():
        return jsonify({
            'status': 401,
            'message': 'Token has been revoked'
        }), 401

    @jwt.unauthorized_loader
    def unauthorized(reason):
        return jsonify({
            'status': 401,
            'message': reason
        }), 401
