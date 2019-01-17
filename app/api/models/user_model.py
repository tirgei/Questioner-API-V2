from ..utils.base_model import Model
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(Model):
    """ Model class for User object """

    table = 'users'

    def save(self, data):
        """ Function to save new user """

        query = "INSERT INTO {} (firstname, lastname, username, email, \
        password) VALUES ('{}', '{}', '{}', '{}', '{}') RETURNING *".format(
            self.table, data['firstname'],
            data['lastname'], data['username'], data['email'],
            generate_password_hash(data['password'])
        )

        self.cur.execute(query)
        result = self.cur.fetchone()

        self.conn.commit()
        return result

    def exists(self, key, value):
        """ Function to check if user exists """

        query = "SELECT * FROM {} WHERE {} = '{}'".format(
            self.table, key, value)
        self.cur.execute(query)

        result = self.cur.fetchall()
        return len(result) > 0

    def where(self, key, value):
        """ Function to fetch user with key, value pair """

        query = "SELECT * FROM {} WHERE {} = '{}'".format(
            self.table, key, value)
        self.cur.execute(query)
        result = self.cur.fetchone()
        return result

    def all(self):
        pass

    def is_admin(self, user_id):
        user = self.where('id', user_id)
        return user['admin']

    @staticmethod
    def checkpassword(hashed_password, password):
        """ Function to check if passwords match """

        return check_password_hash(hashed_password, password)
