from flask import Flask, jsonify
import psycopg2
import os
import time

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_NAME = os.environ.get('POSTGRES_DB', 'callcountdb')
DB_USER = os.environ.get('POSTGRES_USER', 'postgres')
DB_PASS = os.environ.get('POSTGRES_PASSWORD', 'password')

def wait_for_postgres():
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
            conn.close()
            return True
        except psycopg2.OperationalError:
            retries -= 1
            time.sleep(5)
    raise Exception("Postgres is not ready after waiting")

def init_db():
    wait_for_postgres()
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS echos (
            message TEXT,
            count INTEGER
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()
    
@app.route('/echo', methods=['GET'])
def echo():
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()
    cur.execute('SELECT count FROM echos WHERE message = %s', ('echo',))
    row = cur.fetchone()
    if row:
        count = row[0] + 1
        cur.execute('UPDATE echos SET count = %s WHERE message = %s', (count, 'echo'))
    else:
        count = 1
        cur.execute('INSERT INTO echos (message, count) VALUES (%s, %s)', ('echo', count))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "echo", "count": count})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
