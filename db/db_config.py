import sys
import logging
import psycopg2
from instance.config import app_config
from db.db_tables import tables, create_table_queries
from werkzeug.security import generate_password_hash
from psycopg2.extras import RealDictCursor


class DatabaseConnection:

    def init_connection(self, config_name):
        """ Function to initiate db connection """

        config = app_config[config_name]

        database = config.DATABASE_NAME
        user = config.DATABASE_USERNAME
        password = config.DATABASE_PASSWORD
        host = config.DATABASE_HOST
        port = config.DATABASE_PORT

        DSN = 'dbname={} user={} password={} host={} port={}'.format(
            database, user, password, host, port
        )

        try:
            global conn, cur

            conn = psycopg2.connect(DSN)
            cur = conn.cursor(cursor_factory=RealDictCursor)

        except Exception as error:
            print('Error. Unable to establish Database connection')

            logger = logging.getLogger('database')
            logger.error(str(error))

            sys.exit(1)

    def insert(self, query):
        """ Function to insert new item into the db """
        cur.execute(query)
        data = cur.fetchone()
        conn.commit()
        return data

    def fetch_one(self, query):
        """ Function to fetch one item from the db """
        cur.execute(query)
        data = cur.fetchone()
        return data

    def fetch_all(self, query):
        """ Function to fetch all items from the db """
        cur.execute(query)
        data = cur.fetchall()
        return data

    def remove(self, query):
        """ Function to remove item from the db """
        cur.execute(query)
        conn.commit()

    def truncate(self):
        """ Function to truncate database tables """

        cur.execute('TRUNCATE TABLE ' + ','.join(tables) + ' CASCADE')
        conn.commit()

    def drop_tables(self):
        """ Function to drop tables """

        for table in tables:
            cur.execute('DROP TABLE IF EXISTS {} CASCADE'.format(table))

        conn.commit()

    def create_tables(self):
        """ Function to create tables """

        for query in create_table_queries:
            cur.execute(query)

        conn.commit()

    def seed(self):
        """ Function to insert super admin into the db """

        user_query = "SELECT * FROM users WHERE username = 'tirgei'"
        cur.execute(user_query)
        result = cur.fetchone()

        if not result:
            cur.execute("INSERT INTO users (firstname, lastname, username, email,\
            password, admin) VALUES ('Vincent', 'Tirgei', 'tirgei', \
            'admin@app.com', '{}', True)\
            ".format(generate_password_hash('asf8$#Er0')))
            conn.commit()
