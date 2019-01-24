from ..utils.base_model import Model


class QuestionModel(Model):
    """ Model class for question object """

    table = 'questions'

    def all(self, id):
        """ Function to fetch all questions for a meetup """

        query = "SELECT * FROM {} where meetup_id = {}".format(
            self.table, id)

        return self.fetch_all(query)

    def find(self, id):
        pass

    def save(self, data):
        """ Function to save new question """

        query = "INSERT INTO {} (title, body, meetup_id, user_id) \
        VALUES ('{}', '{}', '{}', '{}') RETURNING *".format(
            self.table, data['title'], data['body'], data['meetup_id'],
            data['user_id']
        )

        return self.insert(query)

    def exists(self, key, value):
        """ Function to check if comment exists """

        query = "SELECT * FROM {} WHERE {} = '{}'".format(
            self.table, key, value)

        result = self.fetch_all(query)
        return len(result) > 0

    def upvote(self, question_id):
        """ Function to upvote question """

        question = self.where('id', question_id)
        votes = question['votes'] + 1

        query = "UPDATE {} SET votes = '{}' WHERE id = '{}' \
        RETURNING *".format(self.table, votes, question_id)

        return self.insert(query)

    def downvote(self, question_id):
        """ Function to downvote question """

        question = self.where('id', question_id)
        votes = question['votes'] - 1

        query = "UPDATE {} SET votes = '{}' WHERE id = '{}' \
        RETURNING *".format(self.table, votes, question_id)

        return self.insert(query)

    def where(self, key, value):
        query = "SELECT * FROM {} WHERE {} = '{}'".format(
            self.table, key, value)

        return self.fetch_one(query)

    def delete(self, id):
        pass
