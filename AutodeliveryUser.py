import psycopg2
import db.db_api as db_api

class User:
    def __init__(self,user_id):
        self.user_id = user_id
        self.access_token, self.refresh_token = db_api.get_user_credentials(user_id)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

    @staticmethod
    def register_user(user_id,access_token,refresh_token):
        db_api.register_user(user_id,access_token,refresh_token)
