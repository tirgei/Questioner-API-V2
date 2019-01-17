from .base_test import BaseTest


class TestComment(BaseTest):
    """ Test class for comment endpoints """

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

        self.comment = {
            'body': 'Should include tests in the agenda too'
        }

        self.comment2 = {
            'body': 'Yeah.. they should especially do tests'
        }

        self.client.post('/api/v2/meetups', json=self.meetup,
                         headers=self.headers)
        self.client.post('/api/v2/questions', json=self.question,
                         headers=self.headers)

    def tearDown(self):
        super().tearDown()

    def test_post_comment_question_not_posted(self):
        """ Test post comment to a question that hasn't been posted """

        res = self.client.post('/api/v2/questions/3/comments',
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Question not found')

    def test_post_comment_question_no_data(self):
        """ Test post comment without question data """

        res = self.client.post('/api/v2/questions/1/comments',
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_post_comment_question_empty_data(self):
        """ Test post comment with empty data """

        self.comment.clear()

        res = self.client.post('/api/v2/questions/1/comments',
                               json=self.comment, headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_post_comment(self):
        """ Test post comment successfully """

        res = self.client.post('/api/v2/questions/1/comments',
                               json=self.comment, headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Comment posted successfully')
