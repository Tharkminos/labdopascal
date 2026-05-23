from flask import Flask, render_template
import markdown
app = Flask(__name__)



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
    app.run(debug=True)


