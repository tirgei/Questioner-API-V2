from db.db_config import DatabaseConnection


class RevokedTokenModel(DatabaseConnection):
    """ Model class for revoked tokens """

    table = 'revoked_tokens'

    def save(self, jti):
        """ Function to save new jti """

        query = "INSERT INTO {} (jti) VALUES ('{}') RETURNING *".format(
            self.table, jti)

        self.insert(query)

    def is_blacklisted(self, jti):
        """ Function to check if jti is blacklisted """

        query = "SELECT * FROM {} where jti = '{}'".format(
            self.table, jti)

        result = self.fetch_one(query)
        return bool(result)
