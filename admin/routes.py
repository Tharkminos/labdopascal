from flask import render_template
from . import admin_bp
from .auth import *
from .utils import get_system_info 
@admin_bp.route("/")
@permission_required("admin")
def index():
    return render_template("admin/index.html")



@admin_bp.route("/dashboard")
@permission_required("admin")
def dashboard():

    info = get_system_info()

    return render_template(
        "admin/dashboard.html",
        info=info
    )
