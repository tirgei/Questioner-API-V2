import os
import sys
import logging
import psycopg2
from instance.config import app_config


config_name = os.getenv('APP_ENV')
config = app_config[config_name]


def connect_db():
    """ Function to initialize db connection """

    database = config.DATABASE_NAME
    user = config.DATABASE_USERNAME
    password = config.DATABASE_PASSWORD
    host = config.DATABASE_HOST
    port = config.DATABASE_PORT

    DSN = 'dbname={} user={} password={} host={} port={}'.format(
        database, user, password, host, port
    )

    try:
        conn = psycopg2.connect(DSN)

    except Exception as error:
        print('Error. Unable to establish Database connection')

        logger = logging.getLogger('database')
        logger.error(str(error))

        sys.exit(1)

    return conn
