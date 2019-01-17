from ..utils.base_model import Model


class QuestionModel(Model):
    """ Model class for question object """

    table = 'questions'

    def all(self):
        pass

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
        pass

    def where(self, key, value):
        pass

    def delete(self, id):
        pass
