from ..utils.database_model import DatabaseModel


class RsvpModel(DatabaseModel):
    """ Model class for rsvp """

    table = 'rsvps'

    def save(self, data):
        """ Function to save new rsvp """

        query = "INSERT INTO {} (meetup_id, user_id, response) VALUES\
        ('{}', '{}', '{}') RETURNING *".format(
            self.table, data['meetup_id'], data['user_id'], data['response']
        )

        self.cur.execute(query)
        result = self.cur.fetchone()

        self.conn.commit()
        return result

    def exists(self, meetup_id, user_id):
        """ Function to check user has rsvp """

        query = "SELECT * FROM {} WHERE user_id = '{}' AND meetup_id = '{}'\
        ".format(self.table, user_id, meetup_id)

        self.cur.execute(query)
        result = self.cur.fetchone()
        return bool(result)
