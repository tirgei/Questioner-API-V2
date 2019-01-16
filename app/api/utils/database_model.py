from flask import g
from db.db_config import connect_db
from db.db_tables import create_tables, drop_tables
from .base_model import Model


class DatabaseModel(Model):
    """ Class to initiate database connection """

    def __init__(self):
        self.conn = self.get_db_connection()
        self.cur = self.conn.cursor()

    def get_db_connection(self):
        """ Function to check if database connection exists """

        if 'conn' not in g:
            g.conn = connect_db()
            return g.conn
        return g.conn
