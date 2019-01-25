from db.db_config import DatabaseConnection


class RsvpModel(DatabaseConnection):
    """ Model class for rsvp """

    table = 'rsvps'

    def save(self, data):
        """ Function to save new rsvp """

        query = "INSERT INTO {} (meetup_id, user_id, response) VALUES\
        ('{}', '{}', '{}') RETURNING *".format(
            self.table, data['meetup_id'], data['user_id'], data['response']
        )

        return self.insert(query)

    def exists(self, meetup_id, user_id):
        """ Function to check user has rsvp """

        query = "SELECT * FROM {} WHERE user_id = '{}' AND meetup_id = '{}'\
        ".format(self.table, user_id, meetup_id)

        result = self.fetch_one(query)
        return bool(result)

    def attendees(self, meetup_id):
        """ Function to get number of attendees for a meetup """

        query = "SELECT * FROM {} WHERE meetup_id = '{}' AND response = '{}'\
        ".format(self.table, meetup_id, 'yes')

        result = self.fetch_all(query)
        return len(result)
