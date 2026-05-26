import markdown
import re
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

