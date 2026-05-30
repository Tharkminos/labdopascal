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


# ================= MARKDOWN =================
def renderizar_markdown(arquivo, titulo=None):

    with open(arquivo, encoding="utf-8") as f:
        md = f.read()

    # procura o primeiro H1
    match = re.search(
        r"^#\s+(.+)$",
        md,
        re.MULTILINE
    )

    if match:
        titulo = match.group(1)

    simulacoes = re.findall(
        r"\[simulacao=(.*?)\]",
        md
    )

    for sim in simulacoes:

        md = md.replace(
            f"[simulacao={sim}]",
            f'<div id="canvas-{sim}"></div>'
        )

    html = markdown.markdown(md)

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


# ================= POSTS =================

# Ambiente de testes
@app.route("/teste")
def teste():

    return renderizar_markdown(
        "posts/teste.md",
        "Teste"
    )


# Posts categorizados
@app.route("/posts/<categoria>/<nome>")
def post(categoria, nome):

    arquivo = f"posts/{categoria}/{nome}.md"

    return renderizar_markdown(arquivo)

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

                session["id"] = user[0]
                session["usuario"] = user[1]
                session["email"] = user[2]

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

        # verifica usuário
        cursor.execute(
            """
            SELECT id
            FROM usuarios
            WHERE usuario = ?
            """,
            (usuario,)
        )

        usuario_existente = cursor.fetchone()

        # verifica email
        cursor.execute(
            """
            SELECT id
            FROM usuarios
            WHERE email = ?
            """,
            (email,)
        )

        email_existente = cursor.fetchone()

        if usuario_existente:

            conn.close()

            flash(
                "Nome de usuário já existe",
                "erro"
            )

            return redirect("/register")

        if email_existente:

            conn.close()

            flash(
                "Email já cadastrado",
                "erro"
            )

            return redirect("/register")

        senha_hash = bcrypt.generate_password_hash(
            senha
        ).decode("utf-8")

        cursor.execute(
            """
            INSERT INTO usuarios
            (
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

    session.clear()

    return redirect("/")


# ================= RUN =================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )
