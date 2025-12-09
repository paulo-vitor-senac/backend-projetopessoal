from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "CHAVE_SECRETA_FIXA_AQUI"   # pode ser qualquer coisa segura

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
    return {"status": "ok"}

USUARIO_ADMIN = "pauloadm123"
SENHA_ADMIN = "paulovitor18"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        senha = request.form.get("password")

        if user == USUARIO_ADMIN and senha == SENHA_ADMIN:
            session["logado"] = True
            return redirect("/painel")

        return render_template("login.html", erro="Usuário ou senha incorretos!")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/painel")
def painel():
    if not session.get("logado"):
        return redirect("/login")

    conn = sqlite3.connect("visitas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM access_logs ORDER BY id DESC")
    dados = cursor.fetchall()
    conn.close()

    return render_template("admin-visitas.html", dados=dados)


if __name__ == "__main__":
    app.run(debug=True)