from flask import Flask, jsonify
import psycopg2
import passwords
app = Flask(__name__)

conn = psycopg2.connect(database=passwords.Live.database, user=passwords.Live.user, password=passwords.Live.password, host=passwords.Live.host, port=passwords.Live.port)
cur = conn.cursor()

@app.route('/')
def data():
	cur.execute("SELECT * from STOCKS")
	rows = cur.fetchall()
	conn.close()
	return jsonify(results=rows)
