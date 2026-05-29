from flask import Flask, render_template
import markdown
app = Flask(__name__)
from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
import sqlite3
app = Flask(__name__)
app.secret_key = "B@tman"
bcrypt = Bcrypt(app)

# Página inicial
@app.route("/")
def index():
    return render_template("base.html")

# 🔥 ROTA DINÂMICA
@app.route("/simulacao/<nome>")
def simulacao(nome):
    return render_template("simulacao.html", nome=nome)
@app.route("/atividades/egito")
def egito():
    return render_template("egito.html")
@app.route("/mec")
def mec():
    return render_template("mec.html")
@app.route("/n04")
def atv04():
    return render_template("n04.html")

import re

@app.route("/posts/atom")
def atom():
    with open("posts/atom.md", encoding="utf-8") as f:
        md = f.read()

    simulacoes = re.findall(
        r"\[simulacao=(.*?)\]",
        md
    )

    for sim in simulacoes:

        bloco = f'''
<div id="canvas-{sim}"></div>
'''

        md = md.replace(
            f"[simulacao={sim}]",
            bloco
        )

    html = markdown.markdown(md)

    return render_template(
        "post.html",
        titulo="Átomo",
        conteudo=html,
        simulacoes=simulacoes
    )
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]

        senha = request.form["senha"]

        conn = sqlite3.connect("site.db")

        cursor = conn.cursor()

        cursor.execute(

            "SELECT * FROM usuarios WHERE usuario = ?",

            (usuario,)

        )

        user = cursor.fetchone()

        conn.close()

        if user:

            senha_db = user[2]

            if bcrypt.check_password_hash(senha_db, senha):

                session["usuario"] = usuario

                return redirect("/")

        return "Login inválido"

    return render_template("login.html")
@app.route("/admin")
def admin():

    if "usuario" not in session:

        return redirect("/login")

    return "PAINEL ADMIN"
@app.route("/logout")
def logout():

    session.pop("usuario", None)

    return redirect("/")
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        usuario = request.form["usuario"]

        senha = request.form["senha"]

        senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")

        conn = sqlite3.connect("site.db")

        cursor = conn.cursor()

        cursor.execute(

            "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",

            (usuario, senha_hash)

        )

        conn.commit()

        conn.close()

        return redirect("/login")

    return render_template("register.html")
@app.route("/adm/fe")
def adm_fe():
    with open("posts/adm_fe.md", encoding="utf-8") as f:
        md = f.read()
        html = markdown.markdown(md)
        return render_template(
        "post.html",
        titulo="2ºTRI - FINANÇAS EMPRESARIAIS",
        conteudo=html)
@app.route("/adm/rh")
def adm_rh():
    with open("posts/adm_rh.md", encoding="utf-8") as f:
        md = f.read()
        html = markdown.markdown(md)
        return render_template(
        "post.html",
        titulo="2ºTRI - RECURSOS HUMANOS",
        conteudo=html)

@app.route("/teste")
def teste():

    with open("posts/teste.md", encoding="utf-8") as f:
        md = f.read()

    simulacoes = re.findall(
        r"\[simulacao=(.*?)\]",
        md
    )

    for sim in simulacoes:

        bloco = f'''
<div id="canvas-{sim}"></div>
'''

        md = md.replace(
            f"[simulacao={sim}]",
            bloco
        )

    html = markdown.markdown(md)

    return render_template(
        "post.html",
        titulo="Teste",
        conteudo=html,
        simulacoes=simulacoes
    )
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000,debug=True)


