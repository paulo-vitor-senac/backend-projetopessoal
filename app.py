from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ======= BANCO DE DADOS =======
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

# ======= REGISTRAR VISITA =======
@app.route("/track", methods=["POST"])
def track():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
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

# ======= LISTAR VISITAS =======
@app.route("/visitas", methods=["GET"])
def visitas():
    conn = get_db()
    cursor = conn.execute("SELECT * FROM acessos ORDER BY id DESC")
    dados = cursor.fetchall()
    conn.close()

    visitas = [
        {"id": d[0], "ip": d[1], "user_agent": d[2], "data_hora": d[3]}
        for d in dados
    ]

    return jsonify(visitas)

# ======= ROTA PRINCIPAL =======
@app.route("/")
def home():
    return jsonify({"status": "backend ativo!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
