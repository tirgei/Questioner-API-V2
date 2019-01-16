import unittest
from flask import g
from app import create_app
from manage import migrate, truncate
from app.api.models.user_model import UserModel


class BaseTest(unittest.TestCase):
    """ Base class for tests """

    def setUp(self):
        """ Setup database """

        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.db = UserModel()
        self.client = self.app.test_client()
        migrate(g.conn)

    def tearDown(self):
        """ Clear database """
        truncate(g.conn)
