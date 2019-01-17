from ..utils.base_model import Model


class MeetupModel(Model):
    """ Model class for meetup object """

    table = 'meetups'

    def find(self, id):
        """ Function to fetch specific meetup by id """

        meetup = self.where('id', id)
        return meetup

    def save(self, data):
        """ Function to save new user """

        query = "INSERT INTO {} (topic, description, location, happening_on)\
        VALUES ('{}', '{}', '{}', '{}') RETURNING *".format(
            self.table, data['topic'],
            data['description'], data['location'], data['happening_on']
        )

        self.cur.execute(query)
        result = self.cur.fetchone()

        self.conn.commit()
        return result

    def all(self):
        """ Function to fetch all users """

        query = "SELECT * FROM {}".format(self.table)

        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def exists(self, key, value):
        query = "SELECT * FROM {} WHERE {} = '{}'".format(
            self.table, key, value)
        self.cur.execute(query)

        result = self.cur.fetchall()
        return len(result) > 0

    def where(self, key, value):
        query = "SELECT * FROM {} WHERE {} = '{}'".format(
            self.table, key, value)
        self.cur.execute(query)
        result = self.cur.fetchone()
        return result
