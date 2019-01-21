import os
import unittest
from flask import g
from app import create_app
from db.db_tables import drop_tables, seed
from app.api.models.user_model import UserModel
from app.api.utils.database_model import DatabaseModel


class BaseTest(unittest.TestCase):
    """ Base class for tests """

    def setUp(self):
        """ Setup database """

        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.db = DatabaseModel()
        self.client = self.app.test_client()

        seed(g.conn)
        res = self.client.post('/api/v2/auth/login', json={
            'username': 'tirgei', 'password': 'asf8$#Er0'})

        self.access_token = res.get_json()['access_token']
        self.refresh_token = res.get_json()['refresh_token']
        self.headers = {'Authorization': 'Bearer {}'.format(self.access_token)}

    def tearDown(self):
        """ Clear database """
        drop_tables(g.conn)
