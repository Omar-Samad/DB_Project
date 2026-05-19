from flask import Flask, jsonify, send_file
import mysql.connector

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "seerat2006",  # ← your MySQL password
    "database": "lost_and_found"
}

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/api/lost-items")
def get_lost_items():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM lost_items")
    items = cursor.fetchall()
    conn.close()
    return jsonify(items)

@app.route("/api/found-items")
def get_found_items():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM found_items")
    items = cursor.fetchall()
    conn.close()
    return jsonify(items)

@app.route("/api/matches")
def get_matches():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM matches")
    items = cursor.fetchall()
    conn.close()
    return jsonify(items)

if __name__ == "__main__":
    app.run(debug=True)