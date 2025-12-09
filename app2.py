from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   # libera o acesso do frontend estático

# ==========================
# BANCO DE DADOS
# ==========================

def init_db():
    conn = sqlite3.connect("visitas.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS access_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page TEXT,
            user_agent TEXT,
            ip TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

def registrar_visita(pagina, user_agent, ip):
    conn = sqlite3.connect("visitas.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO access_logs (page, user_agent, ip, timestamp) VALUES (?, ?, ?, ?)",
        (pagina, user_agent, ip, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    conn.close()

@app.route("/log", methods=["POST"])
def log():
    data = request.json
    pagina = data.get("page")
    user_agent = request.headers.get("User-Agent")
    ip = request.remote_addr

    registrar_visita(pagina, user_agent, ip)
    return jsonify({"status": "ok"})


# =====================================
# LOGIN (compatível com frontend estático)
# =====================================

USUARIO_ADMIN = "pauloadm123"
SENHA_ADMIN = "paulovitor18"

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = data.get("username")
    senha = data.get("password")

    if user == USUARIO_ADMIN and senha == SENHA_ADMIN:
        return jsonify({"ok": True})

    return jsonify({"ok": False})


# =======================================================
# API PARA O PAINEL ESTÁTICO BUSCAR AS VISITAS (JSON)
# =======================================================

@app.route("/visitas", methods=["GET"])
def visitas():
    conn = sqlite3.connect("visitas.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, page, user_agent, ip, timestamp FROM access_logs ORDER BY id DESC")
    dados = cursor.fetchall()
    conn.close()

    lista = []
    for row in dados:
        lista.append({
            "id": row[0],
            "page": row[1],
            "user_agent": row[2],
            "ip": row[3],
            "timestamp": row[4]
        })

    return jsonify(lista)


if __name__ == "__main__":
    app.run(debug=True)
