import psycopg2

def get_connection  ():
    return psycopg2.connect('dbname=autodelivery user=postgres')

def register_user  (user_id,access_token,refresh_token):
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

def get_user_credentials  (user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT access_token,refresh_token FROM autodelivery_user WHERE MLID = (%s);',(user_id,))
    response = cur.fetchone()
    cur.close()
    conn.close()
    return response

def get_user_stock_list  (user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''SELECT stock.id,stock.resource,item.name
                FROM stock
                INNER JOIN item
                ON stock.item = item.id
                WHERE item.mluser = %s;''',(user_id,))
    response = cur.fetchall()
    cur.close()
    conn.close()
    return response

def get_user_defined_items  (user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT name,id FROM item where mluser = %s;', (user_id,))
    response = cur.fetchall()
    cur.close()
    conn.close()
    return response

def create_stock(user_id,resource,item_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO stock(resource,item)  VALUES (%s,%s) RETURNING id;',(resource,item_id))
    response = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return response[0]