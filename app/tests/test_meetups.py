from .base_test import BaseTest


class TestMeetup(BaseTest):
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

        self.meetup = {
            'topic': 'Leveling up with Python',
            'description': 'Reprehenderit sunt aliquip aliquip exercitation.',
            'location': 'Andela HQ, Nairobi',
            'happening_on': '30/01/2019'
        }

        self.meetup2 = {
            'topic': 'Android',
            'description': 'Getting started with Kotlin',
            'location': 'Andela HQ, Nairobi',
            'happening_on': '30/01/2019'
        }

    def tearDown(self):
        super().tearDown()

    def test_create_meetup_no_data(self):
        """ Test create meetup with no data sent """

        res = self.client.post('/api/v2/meetups', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_create_meetup_empty_data(self):
        """ Test create meetup with no data sent """

        self.meetup.clear()

        res = self.client.post('/api/v2/meetups', json=self.meetup,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_create_meetup_missing_fields(self):
        """ Test create meetup with missing fields in request """

        self.meetup.pop('location', None)

        res = self.client.post('/api/v2/meetups', json=self.meetup,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data provided')

    def test_create_meetup_empty_fields(self):
        """ Test create meetup with empty fields in request """

        self.meetup.update({'desciption': ''})

        res = self.client.post('/api/v2/meetups', json=self.meetup,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data provided')

    def test_create_meetup(self):
        """ Test create meetup successfully """

        res = self.client.post('/api/v2/meetups', json=self.meetup,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Meetup created successfully')

    def test_create_meetup_invalid_date(self):
        """ Test create meetup with an invalid """

        self.meetup.update({'happening_on': '02/08/19'})

        res = self.client.post('/api/v2/meetups', json=self.meetup,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data provided')

    def test_create_meetup_past_date(self):
        """ Test create meetup with a past date """

        self.meetup.update({'happening_on': '02/08/2018'})

        res = self.client.post('/api/v2/meetups', json=self.meetup,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data provided')

    def test_create_meetup_not_admin(self):
        """ Test create meetup when not admin """

        resp = self.client.post('/api/v2/auth/signup', json=self.user)
        token = resp.get_json()['access_token']
        self.headers.update({'Authorization': 'Bearer {}'.format(token)})

        res = self.client.post('/api/v2/meetups', json=self.meetup,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['status'], 401)
        self.assertEqual(data['message'], 'Not authorized')

    def test_fetch_all_meetups_empty(self):
        """ Test fetch all meetups with none created yet """

        res = self.client.get('/api/v2/meetups')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 0)

    def test_fetch_all_meetups(self):
        """ Test fetch all meetups """

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)
        self.client.post('/api/v2/meetups', json=self.meetup2,
                         headers=self.headers)

        res = self.client.get('/api/v2/meetups')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 2)
