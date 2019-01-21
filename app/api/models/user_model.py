from ..utils.base_model import Model
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(Model):
    """ Model class for User object """

    table = 'users'

    def find(self, id):
        """ Function to fetch single user profile """

        questions_query = "SELECT COUNT(DISTINCT id)\
        FROM questions WHERE user_id = '{}'".format(id)

        self.cur.execute(questions_query)
        questions_asked = self.cur.fetchone()

        comments_query = "SELECT COUNT(DISTINCT question_id)\
        FROM comments WHERE user_id = '{}'".format(id)

        self.cur.execute(comments_query)
        questions_commented = self.cur.fetchone()

        query = "SELECT users.id, users.firstname, users.lastname, users.username\
        FROM users WHERE id = '{}'".format(id)

        self.cur.execute(query)
        result = self.cur.fetchone()

        result.update({
            'questions_asked': questions_asked['count'],
            'questions_commented': questions_commented['count']
            })
        return result

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

    def delete(self, id):
        pass

    def all(self):
        pass

    def is_admin(self, user_id):
        user = self.where('id', user_id)
        return user['admin']

    @staticmethod
    def checkpassword(hashed_password, password):
        """ Function to check if passwords match """

        return check_password_hash(hashed_password, password)
