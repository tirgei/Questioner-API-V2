from .base_test import BaseTest


class TestUser(BaseTest):
    """ Test class for user endpoints """

    def setUp(self):
        super().setUp()

        self.user = {
            'firstname': 'Vincent',
            'lastname': 'Tirgei',
            'username': 'Vinny',
            'email': 'vin@gmail.com',
            'password': 'aanf#244232Y',
            'phonenumber': '0726002063'
        }

    def tearDown(self):
        super().tearDown()

    def test_sign_up_no_data(self):
        """ Test signup with no data sent """

        res = self.client.post('/api/v2/auth/signup')
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_sign_up_empty_data(self):
        """ Test sign up sending empty data """

        self.user.clear()

        res = self.client.post('/api/v2/auth/signup', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_sign_up_empty_fields(self):
        """ Test sign up empty fields """

        self.user.update({'firstname': ''})

        res = self.client.post('/api/v2/auth/signup', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data provided')

    def test_sign_up_invalid_password(self):
        """ Test sign up with an invalid password """

        self.user.update({'password': 'fdsgfgfj'})

        res = self.client.post('/api/v2/auth/signup', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data provided')

    def test_sign_up_invalid_email(self):
        """ Test sign up with an invalid email """

        self.user.update({'email': 'jggmail.com'})

        res = self.client.post('/api/v2/auth/signup', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data provided')

    def test_sign_up_short_password(self):
        """ Test sign up with a short password """

        self.user.update({'password': 'fdsg'})

        res = self.client.post('/api/v2/auth/signup', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data provided')

    def test_sign_up_successfully(self):
        """ Test sign up successfully """

        res = self.client.post('/api/v2/auth/signup', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'User created successfully')

    def test_sign_up_same_username(self):
        """ Test sign up with same username """

        self.client.post('/api/v2/auth/signup', json=self.user)

        self.user.update({
            'firstname': 'John',
            'lastname': 'Doe',
            'email': 'jd@gmail.com'
        })

        res = self.client.post('/api/v2/auth/signup', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['status'], 409)
        self.assertEqual(data['message'], 'Username already exists')

    def test_sign_up_same_email(self):
        """ Test sign up with same email """

        self.client.post('/api/v2/auth/signup', json=self.user)

        self.user.update({
            'firstname': 'John',
            'lastname': 'Doe',
            'username': 'jd'
        })

        res = self.client.post('/api/v2/auth/signup', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['status'], 409)
        self.assertEqual(data['message'], 'Email already exists')
