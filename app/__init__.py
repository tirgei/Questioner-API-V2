from flask import Flask
from instance.config import app_config
from app.api import v2


def create_app(config_name):
    """ Function to initialize Flask app """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    app.register_blueprint(v2)

    return app
