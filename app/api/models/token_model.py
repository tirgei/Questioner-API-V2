from ..utils.database_model import DatabaseModel


class RevokedTokenModel(DatabaseModel):
    """ Model class for revoked tokens """

    table = 'revoked_tokens'

    def save(self, jti):
        """ Function to save new jti """

        query = "INSERT INTO {} (jti) VALUES ('{}')".format(
            self.table, jti)

        self.cur.execute(query)
        self.conn.commit()

    def is_blacklisted(self, jti):
        """ Function to check if jti is blacklisted """

        query = "SELECT * FROM {} where jti = '{}'".format(
            self.table, jti)

        self.cur.execute(query)
        result = self.cur.fetchone()
        return bool(result)
