import os
import unittest
from flask import g
from app import create_app
from db.db_tables import drop_tables
from app.api.models.user_model import UserModel
from app.api.utils.database_model import DatabaseModel


class BaseTest(unittest.TestCase):
    """ Base class for tests """

    def setUp(self):
        """ Setup database """

        os.environ['APP_ENV'] = 'testing'

        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.db = DatabaseModel()
        self.client = self.app.test_client()

    def tearDown(self):
        """ Clear database """
        drop_tables(g.conn)
