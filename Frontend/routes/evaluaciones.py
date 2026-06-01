from flask import Blueprint, render_template
from utils.auth import login_required

evaluaciones_bp = Blueprint("evaluaciones", __name__)


@evaluaciones_bp.route("/evaluaciones",methods=["GET"])
@login_required
def mostrar_evaluaciones():
    return render_template('evaluaciones.html')