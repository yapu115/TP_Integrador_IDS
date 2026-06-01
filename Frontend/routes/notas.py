from flask import Blueprint, render_template
from utils.auth import login_required

notas_bp = Blueprint("notas", __name__)


@notas_bp.route("/notas", methods=["GET"])
@login_required
def mostrar_notas():
    return render_template("notas.html")
