from flask import Blueprint, render_template, session
from utils.auth import login_required

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    nombre = session.get("username", "Usuario")
    return render_template("dashboard.html", nombre=nombre)
