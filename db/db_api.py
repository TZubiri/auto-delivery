import psycopg2

def get_connection():
    return psycopg2.connect('dbname=autodelivery user=postgres')

def register_user(user_id,access_token,refresh_token):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM autodelivery_user WHERE MLID = (%s);',(user_id,))
        response = cur.fetchone()
        if response is None:
            loginResponse = cur.execute('INSERT INTO autodelivery_user VALUES (%s,%s,%s);',(user_id,access_token,refresh_token))
        else:
            loginResponse = cur.execute('UPDATE autodelivery_user SET access_token=%s, refresh_token=%s WHERE mlid=%s;',(access_token,refresh_token,user_id))
        conn.commit()
        cur.close()
        conn.close

def get_user_credentials(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT access_token,refresh_token FROM autodelivery_user WHERE MLID = (%s);',(user_id,))
    return cur.fetchone()