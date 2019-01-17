from ..utils.base_model import Model


class CommentModel(Model):
    """ Model class for comment object """

    table = 'comments'

    def all(self):
        pass

    def find(self, id):
        pass

    def save(self, data):
        """ Function to save new comment """

        query = "INSERT INTO {} (body, question_id, user_id) \
        VALUES ('{}', '{}', '{}') RETURNING *".format(
            self.table, data['body'], data['question_id'], data['user_id']
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
