from flask import Flask, jsonify
from instance.config import app_config
from db.db_config import connect_db
from db.db_tables import create_tables, seed
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
    CORS(app)

    jwt = JWTManager(app)

    try:
        conn = connect_db()
        create_tables(conn)
        seed(conn)

    except Exception as error:
        app.logger.info('Error creating tables: {}'.format(str(error)))

    app.register_blueprint(v2)

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

    return app
