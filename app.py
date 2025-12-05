from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

def get_db():
    conn = sqlite3.connect("visitas.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS acessos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            user_agent TEXT,
            data_hora TEXT
        )
    """)
    return conn

@app.route("/track", methods=["POST"])
def track():
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    conn.execute(
        "INSERT INTO acessos (ip, user_agent, data_hora) VALUES (?, ?, ?)",
        (ip, user_agent, data_hora)
    )
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

@app.route("/visitas")
def visitas():
    conn = get_db()
    cur = conn.execute("SELECT * FROM acessos ORDER BY id DESC")
    dados = cur.fetchall()
    conn.close()

    visitas_formatadas = []
    for v in dados:
        visitas_formatadas.append({
            "id": v[0],
            "ip": v[1],
            "user_agent": v[2],
            "data_hora": v[3]
        })

    return jsonify(visitas_formatadas)

if __name__ == "__main__":
    app.run()
