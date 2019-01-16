from ..utils.base_model import Model
from werkzeug.security import generate_password_hash


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

        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchone()

        self.conn.commit()
        return self.user_dict(result)

    def exists(self, key, value):
        """ Function to check if user exists """

        query = "SELECT * FROM {} WHERE {} = '{}'".format(
            self.table, key, value)
        self.cur.execute(query)

        result = self.cur.fetchall()
        return len(result) > 0

    @staticmethod
    def user_dict(data):
        return {
            'id': data[0],
            'firstname': data[1],
            'lastname': data[2],
            'othername': data[3],
            'username': data[4],
            'phonenumber': data[5],
            'email': data[6],
            'password': data[7],
            'registered': data[8],
            'admin': data[9],
        }
