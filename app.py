from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db():
    conn = sqlite3.connect("visitas.db")
    conn.execute("CREATE TABLE IF NOT EXISTS acessos (id INTEGER PRIMARY KEY AUTOINCREMENT)")
    return conn

@app.route("/track", methods=["POST"])
def track():
    conn = get_db()
    conn.execute("INSERT INTO acessos DEFAULT VALUES")
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

@app.route("/count")
def count():
    conn = get_db()
    cur = conn.execute("SELECT COUNT(*) FROM acessos")
    total = cur.fetchone()[0]
    conn.close()
    return jsonify({"total": total})

if __name__ == "__main__":
    app.run()
