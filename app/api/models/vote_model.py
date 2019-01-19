from ..utils.database_model import DatabaseModel


class VoteModel(DatabaseModel):
    """ Model class for vote """

    table = 'votes'

    def voted(self, question_id, user_id):
        """ Function to check user has voted """

        query = "SELECT * FROM {} WHERE question_id = '{}' AND user_id = '{}'\
        ".format(self.table, question_id, user_id)

        self.cur.execute(query)
        result = self.cur.fetchone()
        return result

    def add(self, data):
        """ Function to add new vote """

        query = "INSERT INTO {} (question_id, user_id, vote) VALUES\
        ('{}', '{}', '{}')".format(
            self.table, data['question_id'], data['user_id'], data['vote']
        )

        self.cur.execute(query)
        self.conn.commit()
