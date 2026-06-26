from flask import render_template
from . import admin_bp


@admin_bp.route("/")
@admin_required("admin")
def index():
    return render_template("admin/index.html")


from .utils import get_system_info 
@admin_bp.route("/dashboard")
@admin_required
def dashboard():

    info = get_system_info()

    return render_template(
        "admin/dashboard.html",
        info=info
    )
