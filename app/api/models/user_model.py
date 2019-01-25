from ..utils.base_model import Model
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(Model):
    """ Model class for User object """

    table = 'users'

    def find(self, id):
        """ Function to fetch single user profile """

        questions_query = "SELECT COUNT(DISTINCT id)\
        FROM questions WHERE user_id = '{}'".format(id)

        comments_query = "SELECT COUNT(DISTINCT question_id)\
        FROM comments WHERE user_id = '{}'".format(id)

        query = "SELECT users.id, users.firstname, users.lastname, users.username\
        FROM users WHERE id = '{}'".format(id)

        questions_asked = self.fetch_one(questions_query)
        questions_commented = self.fetch_one(comments_query)
        result = self.fetch_one(query)

        result.update({
            'questions_asked': questions_asked['count'],
            'questions_commented': questions_commented['count']
            })
        return result

    def save(self, data):
        """ Function to save new user """

        query = "INSERT INTO {} (firstname, lastname, username, phonenumber, email, \
        password) VALUES ('{}', '{}', '{}', '{}', '{}', '{}') RETURNING *".format(
            self.table, data['firstname'],
            data['lastname'], data['username'], data['phonenumber'], data['email'],
            generate_password_hash(data['password'])
        )

        return self.insert(query)

    def exists(self, key, value):
        """ Function to check if user exists """

        query = "SELECT * FROM {} WHERE {} = '{}'".format(
            self.table, key, value)

        result = self.fetch_all(query)
        return len(result) > 0

    def where(self, key, value):
        """ Function to fetch user with key, value pair """

        query = "SELECT * FROM {} WHERE {} = '{}'".format(
            self.table, key, value)
            
        return self.fetch_one(query)

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
