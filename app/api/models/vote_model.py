from db.db_config import DatabaseConnection


class VoteModel(DatabaseConnection):
    """ Model class for vote """

    table = 'votes'

    def voted(self, question_id, user_id):
        """ Function to check user has voted """

        query = "SELECT * FROM {} WHERE question_id = '{}' AND user_id = '{}'\
        ".format(self.table, question_id, user_id)

        return self.fetch_one(query)

    def add(self, data):
        """ Function to add new vote """

        query = "INSERT INTO {} (question_id, user_id, vote) VALUES\
        ('{}', '{}', '{}') RETURNING *".format(
            self.table, data['question_id'], data['user_id'], data['vote']
        )

        self.insert(query)
