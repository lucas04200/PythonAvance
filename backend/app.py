from flask import Flask, request, jsonify
import psycopg2
import os
import time
import requests
import networkx as nx
import json

app = Flask(__name__)

# Configuration de la base de données PostgreSQL
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
        CREATE TABLE IF NOT EXISTS routes (
            id SERIAL PRIMARY KEY,
            start_lat DOUBLE PRECISION,
            start_lon DOUBLE PRECISION,
            end_lat DOUBLE PRECISION,
            end_lon DOUBLE PRECISION,
            path JSONB
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/route', methods=['POST'])
def route():
    data = request.get_json()
    start = (data['start_lat'], data['start_lon'])
    end = (data['end_lat'], data['end_lon'])

    # Requêter l'API OpenStreetMap
    osm_url = f"http://router.project-osrm.org/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}?overview=full"
    response = requests.get(osm_url)
    route_data = response.json()

    if not response.ok or 'routes' not in route_data:
        return jsonify({"error": "Unable to fetch route from OpenStreetMap"}), 500

    # Extraire le chemin
    path = route_data['routes'][0]['geometry']

    # Stocker le chemin dans la base de données
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO routes (start_lat, start_lon, end_lat, end_lon, path)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    ''', (start[0], start[1], end[0], end[1], json.dumps(path)))
    route_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"route_id": route_id, "path": path})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
