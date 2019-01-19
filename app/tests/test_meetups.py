from .base_test import BaseTest


class TestMeetup(BaseTest):
    """ Test class for meetup endpoints """

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
            'happening_on': '22/01/2019'
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

    def test_fetch_upcoming_meetups_empty(self):
        """ Test fetch upcoming meetups with none created yet """

        res = self.client.get('/api/v2/meetups/upcoming')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 0)

    def test_fetch_upcoming_meetups(self):
        """ Test fetch upcoming meetups """

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)
        self.client.post('/api/v2/meetups', json=self.meetup2,
                         headers=self.headers)

        res = self.client.get('/api/v2/meetups/upcoming')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 1)

    def test_fetch_upcoming_meetups_none(self):
        """ Test fetch upcoming meetups with none in the next 1 week"""

        self.meetup.update({'happening_on': '12/02/2019'})

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)
        self.client.post('/api/v2/meetups', json=self.meetup2,
                         headers=self.headers)

        res = self.client.get('/api/v2/meetups/upcoming')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 0)

    def test_fetch_specific_meetup(self):
        """ Test fetch a specific meetup using id """

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)
        self.client.post('/api/v2/meetups', json=self.meetup2,
                         headers=self.headers)

        res = self.client.get('/api/v2/meetups/1')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['data']['id'], 1)

    def test_fetch_non_existent_meetup(self):
        """ Test fetch a non existing meetup """

        res = self.client.get('/api/v2/meetups/10')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Meetup not found')

    def test_delete_meetup_not_created(self):
        """ Test delete meetup that hasn't been created """

        res = self.client.delete('api/v2/meetups/4',
                                 headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Meetup not found')

    def test_delete_meetup(self):
        """ Test delete meetup successfully """

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)

        res = self.client.delete('api/v2/meetups/1', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Meetup deleted successfully')

    def test_delete_meetup_not_admin(self):
        """ Test delete meetup successfully """

        resp = self.client.post('/api/v2/auth/signup', json=self.user)
        token = resp.get_json()['access_token']
        self.headers.update({'Authorization': 'Bearer {}'.format(token)})

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)

        res = self.client.delete('api/v2/meetups/1', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['status'], 401)
        self.assertEqual(data['message'], 'Not authorized')

    def test_rsvps_meetup_not_created(self):
        """ Test RSVP for meetup that hasn't been created """

        res = self.client.post('api/v2/meetups/3/yes', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Meetup not found')

    def test_rsvps_meetup_invalid_rsvp(self):
        """ Test RSVP for meetup that hasn't been created """

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)

        res = self.client.post('api/v2/meetups/1/attending',
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid rsvp')

    def test_rsvps_yes(self):
        """ Test RSVPs yes to a meetup """

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)

        res = self.client.post('api/v2/meetups/1/yes', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Meetup rsvp successfully')
        self.assertEqual(data['data']['response'], 'yes')

    def test_rsvps_no(self):
        """ Test RSVPs no to a meetup """

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)

        res = self.client.post('api/v2/meetups/1/no', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Meetup rsvp successfully')
        self.assertEqual(data['data']['response'], 'no')

    def test_rsvps_maybe(self):
        """ Test RSVPs yes to a meetup """

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)

        res = self.client.post('api/v2/meetups/1/maybe', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Meetup rsvp successfully')
        self.assertEqual(data['data']['response'], 'maybe')

    def test_rsvps_already_responded(self):
        """ Test RSVPs for a meetup already responded to """

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)
        self.client.post('api/v2/meetups/1/maybe', headers=self.headers)

        res = self.client.post('api/v2/meetups/1/maybe', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['status'], 403)
        self.assertEqual(data['message'], 'Meetup already responded')
