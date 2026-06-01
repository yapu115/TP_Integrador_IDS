from flask import Blueprint, render_template
from utils.auth import login_required

asistencia_bp = Blueprint("asistencia", __name__)


@asistencia_bp.route("/asistencia")
@login_required
def asistencia():
    return render_template("asistencia.html")