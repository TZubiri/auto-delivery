import psycopg2


class User:

    def __init__(self,user_id,access_token,refresh_token):
        conn = psycopg2.connect('dbname=autodelivery user=postgres')
        this.user_id = user_id
        this.access_token = access_token
        this.refresh_token = refresh_token
        cur = conn.cursor()
        response = cur.execute('SELECT * FROM autodelivery_user WHERE MLID = (%s)',(user_id,));

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return this.user_id

    @staticmethod
    def user_exists(user_id,conn):
        cur = conn.cursor()
        response = cur.execute('SELECT * FROM autodelivery_user WHERE MLID = (%s)',(user_id,));
