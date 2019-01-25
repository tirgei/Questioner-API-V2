import unittest
from app import create_app
from db.db_config import DatabaseConnection


class BaseTest(unittest.TestCase):
    """ Base class for tests """

    def setUp(self):
        """ Setup database """

        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()

        res = self.client.post('/api/v2/auth/login', json={
            'username': 'tirgei', 'password': 'asf8$#Er0'})

        self.access_token = res.get_json()['access_token']
        self.refresh_token = res.get_json()['refresh_token']
        self.headers = {'Authorization': 'Bearer {}'.format(self.access_token)}

    def tearDown(self):
        """ Clear database """
        db = DatabaseConnection()
        db.init_connection('testing')
        db.drop_tables()
