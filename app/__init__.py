from flask import Flask
from instance.config import app_config
from db.db_config import connect_db
from db.db_tables import create_tables, seed
from app.api import v2
from flask_jwt_extended import (JWTManager)


def create_app(config_name):
    """ Function to initialize Flask app """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    jwt = JWTManager(app)

    conn = connect_db()
    create_tables(conn)
    seed(conn)

    app.register_blueprint(v2)

    return app
