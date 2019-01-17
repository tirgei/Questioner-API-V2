from ..utils.base_model import Model


class QuestionModel(Model):
    """ Model class for question object """

    table = 'questions'

    def all(self, id):
        """ Function to fetch all questions for a meetup """

        query = "SELECT * FROM {} where meetup_id = {}".format(
            self.table, id)

        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def find(self, id):
        pass

    def save(self, data):
        """ Function to save new question """

        query = "INSERT INTO {} (title, body, meetup_id, user_id) \
        VALUES ('{}', '{}', '{}', '{}') RETURNING *".format(
            self.table, data['title'], data['body'], data['meetup_id'],
            data['user_id']
        )

        self.cur.execute(query)
        result = self.cur.fetchone()

        self.conn.commit()
        return result

    def exists(self, key, value):
        """ Function to check if comment exists """

        query = "SELECT * FROM {} WHERE {} = '{}'".format(
            self.table, key, value)
        self.cur.execute(query)

        result = self.cur.fetchall()
        return len(result) > 0

    def where(self, key, value):
        pass

    def delete(self, id):
        pass
