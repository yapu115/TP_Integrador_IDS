from flask import Blueprint, render_template
from utils.auth import login_required

alumnos_bp = Blueprint("alumnos", __name__)

@alumnos_bp.route("/alumnos")
@login_required
def alumnos():
    return render_template("alumnos.html")
