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
            'happening_on': '10/02/2019',
            'tags': ['Python']
        }

        self.meetup2 = {
            'topic': 'Android',
            'description': 'Getting started with Kotlin',
            'location': 'Andela HQ, Nairobi',
            'happening_on': '25/12/2019',
            'tags': ['Android']
        }

    def tearDown(self):
        super().tearDown()

    def test_create_meetup_no_data(self):
        """ Test create meetup with no data sent """

        res = self.client.post('/api/v2/meetups', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided in the request')

    def test_create_meetup_empty_data(self):
        """ Test create meetup with no data sent """

        self.meetup.clear()

        res = self.client.post('/api/v2/meetups', json=self.meetup,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided in the request')

    def test_create_meetup_missing_fields(self):
        """ Test create meetup with missing fields in request """

        self.meetup.pop('location', None)

        res = self.client.post('/api/v2/meetups', json=self.meetup,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['status'], 422)
        self.assertEqual(data['message'], 'Invalid data provided in the request')

    def test_create_meetup_empty_fields(self):
        """ Test create meetup with empty fields in request """

        self.meetup.update({'desciption': ''})

        res = self.client.post('/api/v2/meetups', json=self.meetup,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['status'], 422)
        self.assertEqual(data['message'], 'Invalid data provided in the request')

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

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['status'], 422)
        self.assertEqual(data['message'], 'Invalid data provided in the request')

    def test_create_meetup_past_date(self):
        """ Test create meetup with a past date """

        self.meetup.update({'happening_on': '02/08/2018'})

        res = self.client.post('/api/v2/meetups', json=self.meetup,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['status'], 422)
        self.assertEqual(data['message'], 'Invalid data provided in the request')

    def test_create_meetup_not_admin(self):
        """ Test create meetup when not admin """

        self.client.post('/api/v2/auth/signup', json=self.user)
        resp = self.client.post('/api/v2/auth/login', json=self.user)
        token = resp.get_json()['access_token']
        self.headers.update({'Authorization': 'Bearer {}'.format(token)})

        res = self.client.post('/api/v2/meetups', json=self.meetup,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['status'], 403)
        self.assertEqual(data['message'],
                         'Only admin is authorized to perform this operation')

    def test_create_meetup_same_location_same_topic(self):
        """ Test create meetup at same location and same topic """

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)

        self.meetup.update({'happening_on': '29/03/2019'})
        res = self.client.post('/api/v2/meetups', json=self.meetup,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['status'], 409)

    def test_create_meetup_same_topic_same_day(self):
        """ Test create meetup same topic and same day """

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)

        self.meetup.update({'location': 'ihub'})
        res = self.client.post('/api/v2/meetups', json=self.meetup,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['status'], 409)

    def test_create_meetup_same_location_same_day(self):
        """ Test create meetup same location and same day """

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)

        self.meetup.update({'topic': 'Swift'})
        res = self.client.post('/api/v2/meetups', json=self.meetup,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['status'], 409)

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

        self.meetup.update({'happening_on': '18/02/2019'})

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
        self.assertEqual(data['data']['attendees'], 0)

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

        self.client.post('/api/v2/auth/signup', json=self.user)
        resp = self.client.post('/api/v2/auth/login', json=self.user)
        token = resp.get_json()['access_token']
        self.headers.update({'Authorization': 'Bearer {}'.format(token)})

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)

        res = self.client.delete('api/v2/meetups/1', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['status'], 403)
        self.assertEqual(data['message'], 'Only admin user is authorized to delete meetups')

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
        self.assertEqual(data['message'], 'Invalid rsvp. The allowed options are yes, no or maybe')

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

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['status'], 409)
        self.assertEqual(data['message'], 'Reponse already sent for this meetup')

    def test_fetch_meetup_attendees_none(self):
        """ Test fetch attending users when none has rsvpd """

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)

        res = self.client.get('api/v2/meetups/1/attendees')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['attendees'], 0)
        self.assertEqual(len(data['users']), 0)

    def test_meetup_attendees(self):
        """ Test fetch attending users successfully """

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)

        self.client.post('api/v2/meetups/1/yes', headers=self.headers)

        res = self.client.get('api/v2/meetups/1/attendees')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['attendees'], 1)
        self.assertEqual(len(data['users']), 1)

    def test_fetch_meetup_attendes_not_created(self):
        """ Test fetch attending users when meetup hasn't been created """

        res = self.client.get('api/v2/meetups/1/attendees')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Meetup not found')

    def test_update_meetup_tags_not_created(self):
        """ Test update meetup tags with meetup not created yet """

        res = self.client.patch('/api/v2/meetups/4/tags', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Meetup not found')

    def test_update_meetup_tags_no_data(self):
        """ Test update meetup tags with no data passed """

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)

        res = self.client.patch('/api/v2/meetups/1/tags', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided in the request')

    def test_update_meetup_tags_empty_data(self):
        """ Test update meetup tags with empty data passed """

        tags = {'tags': []}

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)

        res = self.client.patch('/api/v2/meetups/1/tags', json=tags,
                                headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'],
                         'You need to pass atleast 1 tag for the meetup')

    def test_update_meetup_tags_no_tags(self):
        """ Test update meetup tags with no tags passed """

        self.meetup2.pop('tags', None)

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)

        res = self.client.patch('/api/v2/meetups/1/tags', json=self.meetup2,
                                headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No meetup tags provided in the request')

    def test_update_meetup_tags_successfully(self):
        """ Test update meetup tags successfully """

        tags = {'tags': ['Kotlin']}

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)

        res = self.client.patch('/api/v2/meetups/1/tags', json=tags,
                                headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Meetup tags updated successfully')
        self.assertEqual(len(data['data']['tags']), 2)
