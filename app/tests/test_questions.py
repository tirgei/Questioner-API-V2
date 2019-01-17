from .base_test import BaseTest


class TestQuestion(BaseTest):
    """ Test class for question endpoints """

    def setUp(self):
        super().setUp()

        self.meetup = {
            'topic': 'Leveling up with Python',
            'description': 'Reprehenderit sunt aliquip aliquip exercitation.',
            'location': 'Andela HQ, Nairobi',
            'happening_on': '30/01/2019'
        }

        self.question = {
            'title': 'Intro to python',
            'body': 'Are we covering the basics?',
            'meetup_id': 1
        }

        self.question2 = {
            'title': 'Flask',
            'body': 'Are we doing an API?',
            'meetup_id': 1,
        }

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)

    def tearDown(self):
        super().tearDown()

    def test_post_question_meetup_not_created(self):
        """ Test post question to meetup that doesn't exist """

        self.question.update({'meetup_id': 11})

        res = self.client.post('/api/v2/questions', json=self.question,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Meetup not found')

    def test_post_question_without_meetup_id(self):
        """ Test post question to meetup without meetup id """

        self.question.pop('meetup_id', None)

        res = self.client.post('/api/v2/questions', json=self.question,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data provided')

    def post_question_no_data(self):
        """ Test post question with no data sent """

        res = self.client.post('/api/v2/questions', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_post_question_empty_data(self):
        """ Test post question with empty data sent """

        self.question.clear()

        res = self.client.post('/api/v2/questions', json=self.question,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_post_question_missing_fields(self):
        """ Test post question with missing fields in data sent """

        self.question.pop('body', None)

        res = self.client.post('/api/v2/questions', json=self.question,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data provided')

    def test_post_question(self):
        """ Test post question successfully """

        res = self.client.post('/api/v2/questions', json=self.question,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Question posted successfully')

    def test_fetch_all_questions_meetup_not_created(self):
        """ Test fetch all questions for a meetup that doesn't exist """

        res = self.client.get('/api/v2/meetups/13/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Meetup not found')

    def test_fetch_all_questions_empty(self):
        """ Test fetch all questions for a meetup with none posted """

        res = self.client.get('/api/v2/meetups/1/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 0)

    def test_fetch_all_questions(self):
        """ Test fetch all questions for a meetup """

        self.client.post('/api/v2/questions', json=self.question,
                         headers=self.headers)
        self.client.post('/api/v2/questions', json=self.question2,
                         headers=self.headers)

        res = self.client.get('/api/v2/meetups/1/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 2)
