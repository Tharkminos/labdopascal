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
import os

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
    "titulo": "",
    "conteudo": partes[0]
    })

    for i in range(1, len(partes), 2):

        if i + 1 >= len(partes):
            break

        etapas.append({
            "titulo": partes[i].strip(),
            "conteudo": partes[i + 1]
        })

    return etapas
def processar_etapa(conteudo, banco=None):

    checkpoints_html = {}

    # ================= SIMULAÇÕES =================

    simulacoes = re.findall(
        r"\[simulacao=(.*?)\]",
        conteudo
    )

    for sim in simulacoes:

        conteudo = conteudo.replace(
            f"[simulacao={sim}]",
            f'<div id="canvas-{sim}"></div>'
        )

    # ================= CHECKPOINTS =================

    if banco:

        checkpoints = re.findall(
            r"\[checkpoint=(.*?)\]",
            conteudo
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

            marcador = f"@@CHECKPOINT_{indice}@@"

            checkpoints_html[marcador] = html_questao

            conteudo = conteudo.replace(
                f"[checkpoint={dificuldade}]",
                marcador,
                1
            )

    html = markdown.markdown(
        conteudo,
        extensions=["extra"]
    )

    for marcador, html_questao in checkpoints_html.items():

        html = html.replace(
            marcador,
            html_questao
        )

    return html
# ================= MARKDOWN =================
def renderizar_markdown(arquivo, titulo=None,aula_slug=None):

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
    etapas.append({

        "titulo": "Resultados",

        "conteudo": ""
    })

   
    banco = None

    if "questoes" in meta:

        banco = carregar_questoes(
            meta["questoes"]
        )

    for etapa in etapas:

        etapa["conteudo"] = processar_etapa(
            etapa["conteudo"],
            banco
        )
    return render_template(
    "post.html",
    titulo=titulo,
    etapas=etapas,
    simulacoes=re.findall(
        r"\[simulacao=(.*?)\]",
        md
    ),
    meta=meta,
    aula_slug=aula_slug
)

# ================= HOME =================

@app.route("/")
def index():

    return render_template("base.html")

def gerar_estrelas(concluidas, total):

    return (
        "⭐" * concluidas +
        "★" * (total - concluidas)
    )

# ================= ROTA MÓDULOS =========
@app.route("/modulos")
def modulos():

    pasta = "posts/fisica"

    arquivos = os.listdir(pasta)

    modulos = {}

    for arquivo in arquivos:

        if not arquivo.endswith(".md"):
            continue

        nome = arquivo[:-3]

        if "_" not in nome:
            continue

        modulo = nome.rsplit("_", 1)[0]

        if modulo not in modulos:

            modulos[modulo] = []

        modulos[modulo].append(nome)
    for modulo in modulos:
        modulos[modulo].sort(
        key=lambda aula:
        int(
            aula.rsplit("_", 1)[1]
        )
    )
    concluidas = 0
    for aula in aulas_do_modulo:

        if aula in progresso:

            concluidas += 1
    lista_modulos = []

    for slug, aulas in modulos.items():

        primeira_aula = aulas[0]

        titulo = obter_titulo(
            f"posts/fisica/{primeira_aula}.md"
        )

        lista_modulos.append({

            "slug": slug,

            "titulo": titulo,

            "total_aulas": len(aulas)

        })
    proxima = None

    for aula in aulas:

        if aula not in progresso:

            proxima = aula
        break
    return render_template(
    "modulos.html",
    modulos=lista_modulos)

@app.route("/modulo/<slug>")
def modulo(slug):

    pasta = "posts/fisica"

    arquivos = os.listdir(pasta)

    aulas = []

    for arquivo in arquivos:

        if not arquivo.endswith(".md"):
            continue

        nome = arquivo[:-3]

        if not nome.startswith(
            slug + "_"
        ):
            continue

        aulas.append(nome)

    aulas.sort(
        key=lambda aula:
        int(
            aula.rsplit("_", 1)[1]
        )
    )

    lista_aulas = []

    for aula in aulas:

        titulo = obter_titulo(
            f"{pasta}/{aula}.md"
        )

        lista_aulas.append({

            "slug": aula,

            "titulo": titulo

        })

    progresso = []

    if "id" in session:

        conn = sqlite3.connect(
            "site.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT aula
            FROM progresso_aulas
            WHERE usuario_id = ?
            AND concluida = 1
            """,
            (session["id"],)
        )

        resultado = cursor.fetchall()

        progresso = [
            linha[0]
            for linha in resultado
        ]

        conn.close()

    proxima_liberada = False

    for aula in lista_aulas:

        if aula["slug"] in progresso:

            aula["status"] = "concluida"

        elif not proxima_liberada:

            aula["status"] = "proxima"

            proxima_liberada = True

        else:

            aula["status"] = "bloqueada"
    
    return render_template(

        "modulo.html",
        modulo=obter_meta_rapido(f"posts/fisica/{lista_aulas[0]["slug"]}")["titulo_modulo"],

        aulas=lista_aulas

    )
def obter_meta_rapido(arquivo):

    meta = {}

    with open(
        arquivo,
        encoding="utf-8"
    ) as f:

        if f.readline().strip() != "---":
            return meta

        for linha in f:

            linha = linha.strip()

            if linha == "---":
                break

            if ":" in linha:

                chave, valor = linha.split(
                    ":",
                    1
                )

                meta[
                    chave.strip()
                ] = valor.strip()

    return meta
def obter_titulo(arquivo):
    with open(
        arquivo,
        encoding="utf-8"
    ) as f:

        texto = f.read()
    if match:

        return match.group(1)

    return "Sem título"
# ================= POSTS =================
@app.route(
    "/concluir-aula",
    methods=["POST"])
def concluir_aula():

    if "id" not in session:

        return {
            "status":"erro"
        }, 401

    dados = request.get_json()

    aula = dados["aula"]

    nota = dados["nota"]

    xp = dados["xp"]

    conn = sqlite3.connect(
        "site.db"
    )

    cursor = conn.cursor()
    cursor.execute(
    """
    DELETE FROM progresso_aulas
    WHERE usuario_id = ?
    AND aula = ?
    """,
    (
        session["id"],
        aula
    )
)
    cursor.execute(
        """
        INSERT INTO progresso_aulas
        (
            usuario_id,
            aula,
            nota,
            xp_ganho,
            concluida
        )
        VALUES
        (?, ?, ?, ?, 1)
        """,
        (
            session["id"],
            aula,
            nota,
            xp
        )
    )

    conn.commit()

    conn.close()

    return {
        "status":"ok"
    }
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
        arquivo,
        aula_slug=nome
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
