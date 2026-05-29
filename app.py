from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash
)

from flask_bcrypt import Bcrypt

import sqlite3
import markdown
import re


# ================= APP =================

app = Flask(__name__)

app.secret_key = "B@tman"

bcrypt = Bcrypt(app)


# ================= FUNÇÃO POSTS =================

def carregar_post(arquivo, titulo):

    with open(f"posts/{arquivo}", encoding="utf-8") as f:

        md = f.read()

    # procura [simulacao=nome]
    simulacoes = re.findall(
        r"\[simulacao=(.*?)\]",
        md
    )

    # substitui pelo container
    for sim in simulacoes:

        bloco = f'''
<div id="canvas-{sim}"></div>
'''

        md = md.replace(
            f"[simulacao={sim}]",
            bloco
        )

    # markdown -> html
    html = markdown.markdown(
        md,
        extensions=[
            "fenced_code",
            "tables"
        ]
    )

    return render_template(
        "post.html",
        titulo=titulo,
        conteudo=html,
        simulacoes=simulacoes
    )


# ================= PÁGINA INICIAL =================

@app.route("/")
def index():

    return render_template("base.html")


# ================= SIMULAÇÕES =================

@app.route("/simulacao/<nome>")
def simulacao(nome):

    return render_template(
        "simulacao.html",
        nome=nome
    )


@app.route("/atividades/egito")
def egito():

    return render_template("egito.html")


@app.route("/mec")
def mec():

    return render_template("mec.html")


@app.route("/n04")
def atv04():

    return render_template("n04.html")


# ================= POSTS =================

@app.route("/teste")
def teste():

    return carregar_post(
        "teste.md",
        "Teste"
    )


@app.route("/posts/atom")
def atom():

    return carregar_post(
        "atom.md",
        "Átomo"
    )


@app.route("/adm/fe")
def adm_fe():

    return carregar_post(
        "adm_fe.md",
        "2ºTRI - FINANÇAS EMPRESARIAIS"
    )


@app.route("/adm/rh")
def adm_rh():

    return carregar_post(
        "adm_rh.md",
        "2ºTRI - RECURSOS HUMANOS"
    )


# ================= LOGIN =================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        senha = request.form["senha"]

        conn = sqlite3.connect("site.db")

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM usuarios
            WHERE email = ?
            """,
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            senha_db = user[3]

            if bcrypt.check_password_hash(
                senha_db,
                senha
            ):

                session["usuario"] = user[1]

                session["email"] = user[2]

                session["id"] = user[0]

                return redirect("/")
        flash(
                "Email ou senha incorretos",
                "erro"
              )

        return redirect("/login")

    return render_template("login.html")

# ================= REGISTER =================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        usuario = request.form["usuario"]

        email = request.form["email"]

        senha = request.form["senha"]

        conn = sqlite3.connect("site.db")

        cursor = conn.cursor()

        # verifica username
        cursor.execute(
            """
            SELECT id FROM usuarios
            WHERE usuario = ?
            """,
            (usuario,)
        )

        usuario_existente = cursor.fetchone()

        # verifica email
        cursor.execute(
            """
            SELECT id FROM usuarios
            WHERE email = ?
            """,
            (email,)
        )

        email_existente = cursor.fetchone()

        # usuário já existe
        if usuario_existente:

            conn.close()

            flash(
                "Nome de usuário já existe",
                "erro"
            )

            return redirect("/register")

        # email já existe
        if email_existente:

            conn.close()

            flash(
                "Email já cadastrado",
                "erro"
            )

            return redirect("/register")

        # senha hash
        senha_hash = bcrypt.generate_password_hash(
            senha
        ).decode("utf-8")

        # insert
        cursor.execute(
            """
            INSERT INTO usuarios (

                usuario,
                email,
                senha

            )
            VALUES (?, ?, ?)
            """,
            (
                usuario,
                email,
                senha_hash
            )
        )

        conn.commit()

        conn.close()

        flash(
            "Conta criada com sucesso!",
            "sucesso"
        )

        return redirect("/login")

    return render_template("register.html")

# ================= ADMIN =================

@app.route("/admin")
def admin():

    if "usuario" not in session:

        return redirect("/login")

    return "PAINEL ADMIN"


# ================= LOGOUT =================

@app.route("/logout")
def logout():

    session.pop("usuario", None)

    return redirect("/")


# ================= RUN =================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )
