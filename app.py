from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash
)

from admin import admin_bp
from datetime import date, timedelta
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
mapa_conquistas = {
    "atom": 1
}
app.register_blueprint(admin_bp, url_prefix="/admin")
# ================= UTIL =================
def atualizar_banco():

    conn = sqlite3.connect("site.db")

    cursor = conn.cursor()

    cursor.execute(
        "PRAGMA table_info(usuarios)"
    )

    colunas = [
        coluna[1]
        for coluna in cursor.fetchall()
    ]

    if "streak" not in colunas:

        cursor.execute(
            """
            ALTER TABLE usuarios
            ADD COLUMN streak
            INTEGER DEFAULT 0
            """
        )

    if "ultimo_acesso" not in colunas:

        cursor.execute(
            """
            ALTER TABLE usuarios
            ADD COLUMN ultimo_acesso
            TEXT
            """
        )

    conn.commit()

    conn.close()
atualizar_banco()
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
                    if 'true' in valor:
                        dados[chave.strip()] = True
                    elif 'false' in valor:
                        dados[chave.strip()] = False
                    else:
                        dados[chave.strip()] = valor.strip()                        

    return dados, md
def obter_xp_total(usuario_id):
    conn = sqlite3.connect("site.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT xp
        FROM usuarios
        WHERE id = ?
        """,
        (usuario_id,)
    )
    xp = cursor.fetchone()[0]
    conn.close()
    return xp
def calcular_nivel(xp):

    niveis = [
        0,
        100,
        250,
        450,
        700,
        1000,
        1400,
        1900,
        2500
    ]

    nivel = 1

    for i, limite in enumerate(niveis):

        if xp >= limite:

            nivel = i + 1

    return nivel
def dividir_etapas(md, titulo):
    partes = re.split(
        r"\[etapa=(.*?)\]",
        md
    )

    etapas = []

    conteudo = partes[0]

    tipo = "texto"

    if "[simulacao=" in conteudo:

        tipo = "simulacao"

    elif "[checkpoint" in conteudo:

        tipo = "checkpoint"

    etapas.append({

        "titulo": "",

        "conteudo": conteudo,

        "tipo": tipo

    })

    for i in range(1, len(partes), 2):

        if i + 1 >= len(partes):

            break

        conteudo = partes[i + 1]

        tipo = "texto"

        if "[simulacao=" in conteudo:

            tipo = "simulacao"

        elif "[checkpoint" in conteudo:

            tipo = "checkpoint"

        titulo = partes[i].strip()

        etapas.append({
            "titulo": titulo,
            "conteudo": conteudo,
            "tipo": tipo,
            "simulacao": titulo if tipo == "simulacao" else None
        })

    return etapas
def processar_etapa(conteudo, banco=None):
    conteudo = conteudo.replace("þ","&emsp;&emsp;")
    checkpoints_html = {}

    # ================= SIMULAÇÕES =================

    
    centralizar = re.findall(r"→(.*?)←",conteudo)
    for cent in centralizar:
        conteudo = conteudo.replace(
        f"→{cent}←",
        f'<p style="text-align: center;">{cent}</p>'
)
    left = re.findall(r"←(.*?)←",conteudo)
    for cent in left:
        conteudo = conteudo.replace(
        f"←{cent}←",
        f'<p style="text-align: left;">{cent}</p>'
)
    right = re.findall(r"→(.*?)→",conteudo)
    for cent in right:
        conteudo = conteudo.replace(
        f"→{cent}→",
        f'<p style="text-align: right;">{cent}</p>'
)
    justify = re.findall(r"←(.*?)→",conteudo)
    for cent in justify:
        conteudo = conteudo.replace(
        f"←{cent}→",
        f'<p style="text-align: justify;">{cent}</p>'
)
    
    colors = re.findall(r"\[cor=(\d+),(\d+),(\d+),(\d+)\](.*?)\[/cor\]",conteudo)
    for cont in colors:
        r,g,b,a,texto = cont
        antes = f'[cor={r},{g},{b},{a}]{texto}[/cor]' 
        if(int(r)>255): r=255
        if(int(g)>255): g=255
        if(int(b)>255): b=255
        if(int(r)>  1): a=1 
        depois = f'<span style="color: rgba({r},{g},{b},{a});">{texto}</span>'
        conteudo =  conteudo.replace(antes,depois)
    padrao = r"\[simulacao=(.*?)\](?:\s*:::simulacao\s*(.*?)\s*:::)?"
    simulacoes = re.findall(
        padrao,
        conteudo,
        re.DOTALL
    )
    for sim, argumentos in simulacoes:
        argumentos = argumentos.strip()
        chamada = f"""<div id="canvas-{sim}"></div>
    <script>
    {sim}(
        document.getElementById("canvas-{sim}"),
        {{ {argumentos} }}
    );
    </script>"""
        conteudo = re.sub(
            padrao,
            lambda m: chamada,
            conteudo,
            count=1
        )
    # ================= CHECKPOINTS =================

    if banco:

        checkpoints = re.findall(
            r"\[checkpoint=(.*?)\]",
            conteudo
        )

        for indice, dificuldade in enumerate(checkpoints):

            possiveis = [q for q in banco["questoes"] if q["dificuldade"] == dificuldade]

            if not possiveis:
                continue

            questao = random.choice(possiveis)
            possiveis.remove(questao)

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
    if meta.get('results',False) == False:
        etapas.append({

            "titulo": "Resultados",

            "conteudo": "",
            "tipo":"resultado"
        })

   
    banco = None

    if "questoes" in meta:

        banco = carregar_questoes(
            meta["questoes"]
        )
    print("APÓS DIVIDIR")

    for etapa in etapas:
        print(etapa)
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
    arquivo = f"posts/intro.md"

    return renderizar_markdown(
        arquivo)
    

def gerar_estrelas(concluidas, total):

    return (
        "⭐" * concluidas +
        "★" * (total - concluidas)
    )

# ============== PERFIL ====================
@app.route("/perfil")
def perfil():

    try:

        if "id" not in session:
            return redirect("/login")

        usuario_id = session["id"]

        conn = sqlite3.connect("site.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                usuario,
                xp,
                nivel,
                avatar,
                bio,
                streak,
                ultimo_acesso
            FROM usuarios
            WHERE id = ?
            """,
            (usuario_id,)
        )

        resultado = cursor.fetchone()

        if resultado is None:
            conn.close()
            return redirect("/login")

        (
            usuario,
            xp_total,
            _,
            avatar,
            bio,
            streak,
            ultimo_acesso
        ) = resultado

        nivel = calcular_nivel(xp_total)

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM progresso_aulas
            WHERE usuario_id = ?
            AND concluida = 1
            """,
            (usuario_id,)
        )

        aulas = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM user_achievements
            WHERE usuario_id = ?
            """,
            (usuario_id,)
        )

        conquistas = cursor.fetchone()[0]

        conn.close()

        hoje = str(date.today())
        ontem = str(date.today() - timedelta(days=1))

        if ultimo_acesso == hoje:
            emoji = "🔥"

        elif ultimo_acesso == ontem:
            emoji = "⏳"

        else:
            emoji = "❌"

        return render_template(

            "perfil.html",

            nome=usuario,

            emoji=emoji,

            xp_total=xp_total,

            nivel=nivel,

            avatar=avatar,

            bio=bio,

            aulas=aulas,

            conquistas=conquistas,

            streak=streak

        )

    except Exception as error:

        return str(error)
@app.route("/ranking")
def ranking():

    conn = sqlite3.connect(
        "site.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            usuario,
            xp,
            streak
        FROM usuarios
        ORDER BY xp DESC
        LIMIT 10
        """
    )

    ranking = cursor.fetchall()

    posicao_usuario = None

    if "id" in session:

        cursor.execute(
            """
            SELECT COUNT(*) + 1
            FROM usuarios
            WHERE xp >
            (
                SELECT xp
                FROM usuarios
                WHERE id = ?
            )
            """,
            (
                session["id"],
            )
        )

        posicao_usuario = (
            cursor.fetchone()[0]
        )

        cursor.execute(
            """
            SELECT
                usuario,
                xp,
                streak
            FROM usuarios
            WHERE id = ?
            """,
            (
                session["id"],
            )
        )

        usuario_logado = (
            cursor.fetchone()
        )

    else:

        usuario_logado = None

    conn.close()

    return render_template(

        "ranking.html",

        ranking=ranking,

        usuario_logado=usuario_logado,

        posicao_usuario=posicao_usuario

    )# ============== DEBUG NIVEL ===============
@app.route("/debug-nivel")
def debug_nivel():

    xp = obter_xp_total(
        session["id"]
    )

    return {

        "xp": xp,

        "nivel":
        calcular_nivel(xp)

    }
# ================= ROTA MÓDULOS =========

@app.route("/modulos")
def modulos():

    pasta = "posts/fisica"

    arquivos = os.listdir(pasta)

    modulos = {}
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

       progresso = [
        linha[0]
        for linha in cursor.fetchall()
    ]

       conn.close()

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
    
    lista_modulos = []

    for slug, aulas in modulos.items():
        concluidas = 0
        for aula in aulas:
           if aula in progresso:
              concluidas += 1
        primeira_aula = aulas[0]
        proxima = None
        total_aulas = len(aulas)
        percentual = 0
        nivel = min(5,((total_aulas - 1) // 5) + 1)
        estrelas = ("⭐" * nivel +"★" * (5 - nivel))
        if total_aulas > 0:
            percentual = round(
                concluidas * 100 /
                total_aulas
            )

        titulo = obter_titulo(
            f"posts/fisica/{primeira_aula}.md"
        )
        with open(f"posts/fisica/{primeira_aula}.md", "r", encoding="utf-8") as f:
            conteudo = f.read()
        meta,md = ler_metadados(conteudo)
        img = meta.get("imagem_modulo","generic_module.webp")
        lista_modulos.append({
            "slug": slug,
            "titulo": titulo,
            "total_aulas": total_aulas,
            "concluidas": concluidas,
            "percentual": percentual,
            "estrelas": estrelas,
            "proxima": proxima,
            "imagem":img
        })
    
    for aula in aulas:

        if aula not in progresso:
            proxima = aula
            break
    return render_template(
    "modulos.html",
    modulos=lista_modulos)
def atualizar_streaks():

    ontem = str(date.today() - timedelta(days=1))

    conn = sqlite3.connect("site.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE usuarios
        SET streak = 0
        WHERE ultimo_acesso IS NOT NULL
          AND ultimo_acesso < ?
          AND streak > 0
        """,
        (ontem,)
    )

    conn.commit()

    alterados = cursor.rowcount

    conn.close()

    return alterados
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
    concluidas = 0

    for aula in lista_aulas:

        if aula["slug"] in progresso:

            concluidas += 1

    total_aulas = len(lista_aulas)

    percentual = 0

    if total_aulas > 0:

        percentual = round(
            concluidas * 100 /
            total_aulas
        )
    for aula in lista_aulas:

        if aula["slug"] in progresso:

            aula["status"] = "concluida"

        elif not proxima_liberada:

            aula["status"] = "proxima"

            proxima_liberada = True

        else:

            aula["status"] = "bloqueada"
    

    meta_modulo = obter_meta_rapido(
        f"posts/fisica/{lista_aulas[0]['slug']}.md"
    )

    titulo_modulo = meta_modulo.get(
        "titulo_modulo",
        "Sem título"
    )

    descricao_modulo = meta_modulo.get(
        "descricao_modulo",
        ""
    )

    imagem_modulo = meta_modulo.get(
        "imagem_modulo",
        "generic_module.webp"
    )
    return render_template(
        "modulo.html",
        modulo=titulo_modulo,
        descricao=descricao_modulo,
        imagem=imagem_modulo,
        aulas=lista_aulas,
        concluidas=concluidas,
        total_aulas=total_aulas,
        percentual=percentual
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
       match = re.search(
       r"^#\s*(.+)$",
       texto,
       re.MULTILINE
)
    
    if match:

        return match.group(1)

    return "Sem título"
def desbloquear_conquista(
    usuario_id,
    achievement_id
):

    conn = sqlite3.connect(
        "site.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM user_achievements
        WHERE usuario_id = ?
        AND achievement_id = ?
        """,
        (
            usuario_id,
            achievement_id
        )
    )

    if cursor.fetchone():

        conn.close()

        return False

    cursor.execute(
        """
        INSERT INTO user_achievements
        (
            usuario_id,
            achievement_id,
            data_desbloqueio
        )
        VALUES
        (
            ?, ?, datetime('now')
        )
        """,
        (
            usuario_id,
            achievement_id
        )
    )

    conn.commit()

    conn.close()

    return True
# ================= POSTS =================
@app.route(
    "/concluir-aula",
    methods=["POST"])
def concluir_aula():
    try:        
        xp_bonus = 0
        if "id" not in session:
    
            return {
                "status":"erro"
            }, 401
        
        dados = request.get_json()
    
        aula = dados["aula"]
    
        nota = dados["nota"]
    
        xp = dados["xp"]
        xp_antes = obter_xp_total(session["id"])
    
        nivel_antes = calcular_nivel(xp_antes)
        conn = sqlite3.connect(
            "site.db"
        )
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT concluida
            FROM progresso_aulas
            WHERE usuario_id = ?
            AND aula = ?
            """,
            (
                session["id"],
                aula
            )
        )
        registro_existente = cursor.fetchone()


        from datetime import date, timedelta
        cursor.execute(
            """
            SELECT streak,
                   ultimo_acesso
            FROM usuarios
            WHERE id = ?
            """,
            (
                session["id"],
            )
        )

        streak_atual, ultimo_acesso = (
            cursor.fetchone()
        )
        hoje = date.today()
        ontem = hoje - timedelta(days=1)
        novo_streak = streak_atual
        if ultimo_acesso is None:

            novo_streak = 1

        elif ultimo_acesso == str(hoje):

            novo_streak = streak_atual

        elif ultimo_acesso == str(ontem):

            novo_streak = streak_atual + 1

        else:
            novo_streak = 1
        cursor.execute(
            """
            UPDATE usuarios
            SET streak = ?,
                ultimo_acesso = ?
            WHERE id = ?
            """,
            (
                novo_streak,
                str(hoje),
                session["id"]
            )
        )

        conn.commit()
    
        


    
        revisao = False
        if registro_existente:
            revisao = True
    
            xp = 5
    
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
        cursor.execute(
        """
        UPDATE usuarios
        SET xp = xp + ?
        WHERE id = ?
        """,
        (
            xp,
            session["id"]
            )
        )
    
        conn.commit()
        modulo = aula.split("_")[0]
    
        total_aulas = 0
    
        for arquivo in os.listdir(
            "posts/fisica"
        ):
    
            if (
                arquivo.startswith(
                    modulo + "_"
                )
                and
                arquivo.endswith(".md")
            ):
    
                total_aulas += 1   
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM progresso_aulas
            WHERE usuario_id = ?
            AND aula LIKE ?
            AND concluida = 1
            """,
            (
                session["id"],
                modulo + "_%"
            )
        )
        concluidas = cursor.fetchone()[0]
        conquista_desbloqueada = False
        if concluidas >= total_aulas:
            if modulo in mapa_conquistas:
                conquista_desbloqueada = (
                    desbloquear_conquista(
                        session["id"],
                        mapa_conquistas[modulo]
                    )
                )
    
                if conquista_desbloqueada:
    
                    xp_bonus = 50
    
    
        if xp_bonus > 0:
            cursor.execute(
                """
                UPDATE usuarios
                SET xp = xp + ?
                WHERE id = ?
                """,
                (
                    xp_bonus,
                    session["id"]
                )
            )
    
            conn.commit()
        xp_depois = obter_xp_total(
            session["id"]
        )
    
        nivel_depois = calcular_nivel(
            xp_depois
        )
    
        nivel_up = (
            nivel_depois >
            nivel_antes
        )
        conn.close()
        return {
    
        "status":"ok",
    
        "conquista":conquista_desbloqueada,
    
        "revisao":revisao,
    
        "xp_bonus":xp_bonus,
    
        "nivel_up":nivel_up,
    
        "nivel":nivel_depois,
         "xp":xp
    
    }
    except Exception as error:
        return {"erro": str(error)}, 500
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
@app.route("/auth")
def auth():

    if "id" not in session:
        return "", 401

    # Opcional
    if not session.get("admin"):
         return "", 403

    return "", 200
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        senha = request.form["senha"]

        conn = sqlite3.connect("site.db")

        cursor = conn.cursor()

        cursor.execute("""
        SELECT
            id,
            usuario,
            email,
            senha,
            admin,
            professor,
            monitor
        FROM usuarios
        WHERE email = ?
        """, (email,))
        
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

                session["admin"] = bool(user[4])
                session["professor"] = bool(user[5])
                session["monitor"] = bool(user[6])
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



# ================= CONQUISTAS =================
@app.route("/conquistas")
def conquistas():

    if "id" not in session:

        return redirect("/login")

    conn = sqlite3.connect(
        "site.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            a.id,
            a.nome,
            a.descricao,
            ua.data_desbloqueio
        FROM achievements a

        LEFT JOIN
        user_achievements ua

        ON a.id = ua.achievement_id

        AND ua.usuario_id = ?
        """,
        (
            session["id"],
        )
    )

    resultado = cursor.fetchall()

    conn.close()

    lista = []

    for linha in resultado:

        lista.append({

            "id": linha[0],

            "nome": linha[1],

            "descricao": linha[2],

            "desbloqueada":
                linha[3] is not None,

            "data":
                linha[3]

        })

    return render_template(

        "conquistas.html",

        conquistas=lista

    )



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
