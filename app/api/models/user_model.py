from ..utils.base_model import Model
from werkzeug.security import generate_password_hash


class UserModel(Model):
    """ Model class for User object """

    table = 'users'

    def save(self, data):
        """ Function to save new user """

        query = "INSERT INTO {} (firstname, lastname, username, email, \
        password) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
            self.table, data['firstname'],
            data['lastname'], data['username'], data['email'],
            generate_password_hash(data['password'])
        )

        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def exists(self, key, value):
        """ Function to check if user exists """

        query = "SELECT * FROM {} WHERE {} = '{}'".format(
            self.table, key, value)
        self.cur.execute(query)
        result = self.cur.fetchall()

        return len(result) > 0
