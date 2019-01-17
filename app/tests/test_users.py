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

    def test_login_no_data(self):
        """ Test login with no data provided """

        res = self.client.post('/api/v2/auth/login')
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_login_empty_data(self):
        """ Test login with empty data provided """

        self.user.clear()

        res = self.client.post('/api/v2/auth/login', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_login_unregistered_user(self):
        """ Test login with unregistered user credentials """

        res = self.client.post('/api/v2/auth/login', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'User not found')

    def test_login_successfully(self):
        """ Test successfull login """

        self.client.post('/api/v2/auth/signup', json=self.user)

        res = self.client.post('/api/v2/auth/login', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'User logged in successfully')

    def test_login_no_username_provided(self):
        """ Test login with no username provided """

        self.client.post('/api/v2/auth/signup', json=self.user)
        self.user.pop('username', None)

        res = self.client.post('/api/v2/auth/login', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid credentials')

    def test_login_invalid_password(self):
        """ Test login with invalid password """

        self.client.post('/api/v2/auth/signup', json=self.user)
        self.user.update({'password': 'asfdgfdngf'})

        res = self.client.post('/api/v2/auth/login', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data provided')

    def test_login_incorrect_password(self):
        """ Test login with invalid password """

        self.client.post('/api/v2/auth/signup', json=self.user)
        self.user.update({'password': 'zdf7#sdfN'})

        res = self.client.post('/api/v2/auth/login', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['status'], 422)
        self.assertEqual(data['message'], 'Incorrect password')
