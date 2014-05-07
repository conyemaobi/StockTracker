from flask import Flask, jsonify
import psycopg2
app = Flask(__name__)

cur = conn.cursor()

@app.route('/')
def data():
	cur.execute("SELECT * from STOCKS")
	rows = cur.fetchall()
	conn.close()
	return jsonify(results=rows)
