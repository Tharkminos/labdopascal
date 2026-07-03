from flask import (
    render_template,
    redirect,
    url_for,
    request
)
from . import admin_bp
from .auth import *
from .utils import get_system_info 
import subprocess
@admin_bp.route("/")
@permission_required("admin")
def index():
    return render_template("admin/index.html")


@permission_required("admin")
@admin_bp.route("/dashboard")
def dashboard():

    info = get_system_info()

    return render_template(
        "admin/dashboard.html",
        info=info
    )

@permission_required("admin")
@admin_bp.route("/git")

def admin_git():
    pasta = "/var/www/labdopascal"

    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=pasta,
        capture_output=True,
        text=True
    ).stdout.strip()

    ultimo_commit = subprocess.run(
        ["git", "log", "-1", "--pretty=%B"],
        cwd=pasta,
        capture_output=True,
        text=True
    ).stdout.strip()

    arquivos = subprocess.run(
        ["git", "status", "--short"],
        cwd=pasta,
        capture_output=True,
        text=True
    ).stdout.strip()

    return render_template(

        "admin/git.html",

        branch=branch,

        ultimo_commit=ultimo_commit,

        arquivos=arquivos,

        resultado=None

    )

@permission_required("admin")
@admin_bp.route("/git/status",methods=["POST"])
def git_status():
    return redirect(url_for("admin.admin_git"))

@permission_required("admin")
@admin_bp.route("/git/pull", methods=["POST"])

def git_pull():
    pasta = "/var/www/labdopascal"

    resultado = subprocess.run(

        ["git", "pull"],

        cwd=pasta,

        capture_output=True,

        text=True

    )

    return render_template(

        "admin/git.html",

        branch=subprocess.run(
            ["git","branch","--show-current"],
            cwd=pasta,
            capture_output=True,
            text=True
        ).stdout.strip(),

        ultimo_commit=subprocess.run(
            ["git","log","-1","--pretty=%B"],
            cwd=pasta,
            capture_output=True,
            text=True
        ).stdout.strip(),

        arquivos=subprocess.run(
            ["git","status","--short"],
            cwd=pasta,
            capture_output=True,
            text=True
        ).stdout.strip(),

        resultado=resultado.stdout + resultado.stderr

    )

@admin_bp.route("/restart", methods=["POST"])
@permission_required("admin")
def restart_services():

    try:
        subprocess.run(
            ["sudo", "/usr/bin/systemctl", "restart", "pascal.service"],
            check=True
        )
        subprocess.run(
            ["sudo", "/usr/bin/systemctl", "restart", "nginx.service"],
            check=True
        )

        return render_template(
            "admin/git.html",  # ou seu dashboard admin
            resultado="🚀 Serviços reiniciados com sucesso!"
        )

    except subprocess.CalledProcessError as e:
        return render_template(
            "admin/git.html",
            resultado=f"❌ Erro ao reiniciar serviços: {str(e)}"
        )

