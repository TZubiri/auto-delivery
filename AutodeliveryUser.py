import psycopg2
import db.db_api as db_api

class User:
    def __init__(self,user_id,access_token = None,refresh_token = None):
        self.user_id = user_id
        if access_token = None:
            self.access_token, self.refresh_token = db_api.get_user_credentials(user_id)
        else:
            self.access_token = access_token
            self.refresh_token = refresh_token
            db_api.register_user(user_id,access_token,refresh_token)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

