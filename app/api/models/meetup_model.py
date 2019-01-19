from ..utils.base_model import Model
from datetime import datetime, timedelta


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

    def delete(self, id):
        """ Function to delete meetup """

        query = "DELETE FROM {} WHERE id = {}".format(self.table, id)
        self.cur.execute(query)
        self.conn.commit()
        return True

    def upcoming(self):
        """ Fetch upcoming meetups in the next 1 week """

        today = datetime.now().strftime('%d/%m/%Y')
        last_day = (datetime.now() + timedelta(days=7)).strftime('%d/%m/%Y')

        query = "SELECT * FROM {} WHERE happening_on BETWEEN\
        '{}' AND '{}'".format(self.table, today, last_day)

        self.cur.execute(query)
        result = self.cur.fetchall()
        return result
