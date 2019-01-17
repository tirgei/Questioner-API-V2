from flask import g
from db.db_config import connect_db
from psycopg2.extras import RealDictCursor


class DatabaseModel():
    """ Class to initiate database connection """

    def __init__(self):
        self.conn = self.get_db_connection()
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    @staticmethod
    def get_db_connection():
        """ Function to check if database connection exists """

        if 'conn' not in g:
            g.conn = connect_db()
            return g.conn
        return g.conn
