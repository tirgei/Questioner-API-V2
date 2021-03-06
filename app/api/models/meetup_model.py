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
        """ Function to save new meetup """

        tags = '{'

        for tag in data['tags']:
            tags += '"' + tag + '",'

        tags = tags[:-1] + '}'

        query = "INSERT INTO {} (topic, description, tags, location, happening_on)\
        VALUES ('{}', '{}', '{}', '{}', '{}') RETURNING *".format(
            self.table, data['topic'], data['description'], tags,
            data['location'], data['happening_on']
        )

        return self.insert(query)

    def all(self):
        """ Function to fetch all meetups """

        query = "SELECT * FROM {}".format(self.table)

        return self.fetch_all(query)

    def exists(self, key, value):
        query = "SELECT * FROM {} WHERE {} = '{}'".format(
            self.table, key, value)

        result = self.fetch_all(query)
        return len(result) > 0

    def where(self, key, value):
        query = "SELECT * FROM {} WHERE {} = '{}'".format(
            self.table, key, value)

        return self.fetch_one(query)

    def delete(self, id):
        """ Function to delete meetup """

        query = "DELETE FROM {} WHERE id = {}".format(self.table, id)

        self.remove(query)
        return True

    def upcoming(self):
        """ Fetch upcoming meetups in the next 1 week """

        today = datetime.now().strftime("%Y-%m-%d")
        last_day = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        query = "SELECT * FROM {} WHERE happening_on BETWEEN\
        '{}' AND '{}'".format(self.table, today, last_day)

        return self.fetch_all(query)

    def attendees(self, meetup_id):
        """ Fetch all attendees for an upcoming meetup """

        query = "SELECT id, firstname, lastname, username FROM users WHERE\
        id IN ( SELECT user_id FROM rsvps WHERE meetup_id = '{}' AND response \
        = 'yes')".format(meetup_id)

        return self.fetch_all(query)

    def update_tags(self, meetup_id, meetup_tags):
        """ Function to update meetup tags """

        meetup = self.where('id', meetup_id)
        new_tags = list(set(meetup_tags + meetup['tags']))

        tags = '{'

        for tag in new_tags:
            tags += '"' + tag + '",'

        tags = tags[:-1] + '}'

        query = "UPDATE {} SET tags = '{}' WHERE id = '{}' \
        RETURNING *".format(self.table, tags, meetup_id)

        return self.insert(query)

    def check_if_duplicate(self, data):
        """ Check if meetup is a duplicated of another meetup """

        query = "SELECT * FROM {} WHERE topic = '{}' AND location = '{}'\
        ".format(self.table, data['topic'], data['location'])

        result = self.fetch_one(query)
        if result:
            return True, 'Meetup with same topic at the same venue\
            already exists'

        query = "SELECT * FROM {} WHERE happening_on = '{}' AND location = '{}'\
        ".format(self.table, data['happening_on'], data['location'])

        result = self.fetch_one(query)
        if result:
            return True, 'Meetup happening the same date at the same venue \
            already exists'

        query = "SELECT * FROM {} WHERE topic = '{}' AND happening_on = '{}'\
        ".format(self.table, data['topic'], data['happening_on'])

        result = self.fetch_one(query)
        if result:
            return True, 'Meetup happening the same date with same topic \
            already exists'

        return False, None
