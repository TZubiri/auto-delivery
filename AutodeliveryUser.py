import psycopg2
import db.db_api as db_api

class User:
    def __init__(self,user_id,access_token = None,refresh_token = None):
        self.user_id = user_id
        if access_token == None:
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

    def is_authenticated(self):
        return True

    def stock_list(self):
        ls = []
        for raw_stock in db_api.get_user_stock_list(self.user_id):
            ls.append(Stock(int(raw_stock[0]),raw_stock[1],raw_stock[2]))
        return ls

    def defined_items(self):
        return db_api.get_user_defined_items(self.user_id)




class Stock():
    def __init__(self,id:int,resource:str,item_name:str):
        self.id = id
        self.resource = resource
        self.item_name = item_name
