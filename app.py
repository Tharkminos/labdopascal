from flask import Flask, render_template
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

if __name__ == "__main__":
    app.run(debug=True)


