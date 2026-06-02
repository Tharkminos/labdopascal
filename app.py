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
import json
import random


# ================= APP =================

app = Flask(__name__)

app.secret_key = "B@tman"

bcrypt = Bcrypt(app)


# ================= UTIL =================

def carregar_questoes(nome):

    with open(
        f"questoes/fisica/{nome}.json",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def ler_metadados(md):

    dados = {}

    if md.startswith("---"):

        partes = md.split("---", 2)

        if len(partes) >= 3:

            cabecalho = partes[1]

            md = partes[2]

            for linha in cabecalho.splitlines():

                if ":" in linha:

                    chave, valor = linha.split(":", 1)

                    dados[chave.strip()] = valor.strip()

    return dados, md
def dividir_etapas(md, titulo):

    partes = re.split(
        r"\[etapa=(.*?)\]",
        md
    )

    etapas = []

    etapas.append({
        "titulo": titulo,
        "conteudo": partes[0]
    })

    for i in range(1, len(partes), 2):

        etapas.append({
            "titulo": partes[i],
            "conteudo": partes[i + 1]
        })

    return etapas

# ================= MARKDOWN =================
def renderizar_markdown(arquivo, titulo=None):

    with open(
        arquivo,
        encoding="utf-8"
    ) as f:

        md = f.read()

    meta, md = ler_metadados(md)
    # ================= TÍTULO =================

    if titulo is None:

        match = re.search(
            r"^#\s*(.+)$",
            md,
            re.MULTILINE
        )

        if match:

            titulo = match.group(1).strip()

            md = re.sub(
                r"^#\s*.+$\n?",
                "",
                md,
                count=1,
                flags=re.MULTILINE
            )

        else:

            titulo = "Sem título"
        etapas = dividir_etapas(md,titulo)

    # ================= SIMULAÇÕES =================

    simulacoes = re.findall(
        r"\[simulacao=(.*?)\]",
        md
    )

    for sim in simulacoes:

        md = md.replace(
            f"[simulacao={sim}]",
            f'<div id="canvas-{sim}"></div>'
        )

    # ================= CHECKPOINTS =================

    checkpoints_html = {}

    if "questoes" in meta:

        banco = carregar_questoes(
            meta["questoes"]
        )

        checkpoints = re.findall(
            r"\[checkpoint=(.*?)\]",
            md
        )

        for indice, dificuldade in enumerate(checkpoints):

            possiveis = [

                q

                for q in banco["questoes"]

                if q["dificuldade"] == dificuldade

            ]

            if not possiveis:

                continue

            questao = random.choice(
                possiveis
            )

            alternativas_html = ""

            for i, alternativa in enumerate(
                questao["alternativas"]
            ):

                correta = int(
                    i == questao["correta"]
                )

                alternativas_html += f"""
                <button
                    class="alternativa"
                    data-correta="{correta}"
                >
                    {alternativa}
                </button>
                """

            html_questao = f"""
            <div class="checkpoint">

                <p class="checkpoint-pergunta">
                    {questao["pergunta"]}
                </p>

                <div class="checkpoint-alternativas">

                    {alternativas_html}

                </div>

                <div class="checkpoint-feedback"></div>

            </div>
            """

            marcador = (
                f"@@CHECKPOINT_{dificuldade.upper()}_{indice}@@"
            )

            checkpoints_html[marcador] = html_questao

            md = md.replace(
                f"[checkpoint={dificuldade}]",
                marcador,
                1
            )

    # ================= HTML =================

    html = markdown.markdown(
        md,
        extensions=["extra"]
    )

    for marcador, html_questao in checkpoints_html.items():

        html = html.replace(
            marcador,
            html_questao
        )
    for etapa in etapas:
        etapa["conteudo"] = markdown.markdown(
            etapa["conteudo"],
            extensions=["extra"]
    )
    return render_template(
        "post.html",
        etapas=etapas,
        titulo=titulo,
        conteudo=html,
        simulacoes=simulacoes,
        meta=meta
    )

# ================= HOME =================

@app.route("/")
def index():

    return render_template("base.html")


# ================= POSTS =================

@app.route("/teste")
def teste():

    return renderizar_markdown(
        "posts/teste.md",
        "Teste"
    )


@app.route("/posts/<categoria>/<nome>")
def post(categoria, nome):

    arquivo = f"posts/{categoria}/{nome}.md"

    return renderizar_markdown(
        arquivo
    )


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
            SELECT *
            FROM usuarios
            WHERE email = ?
            """,
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            if bcrypt.check_password_hash(
                user[3],
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

        cursor.execute(
            """
            SELECT id
            FROM usuarios
            WHERE usuario = ?
            """,
            (usuario,)
        )

        if cursor.fetchone():

            conn.close()

            flash(
                "Nome de usuário já existe",
                "erro"
            )

            return redirect("/register")

        cursor.execute(
            """
            SELECT id
            FROM usuarios
            WHERE email = ?
            """,
            (email,)
        )

        if cursor.fetchone():

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
