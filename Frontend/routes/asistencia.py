from flask import Blueprint, render_template

asistencia_bp = Blueprint("asistencia", __name__)


@asistencia_bp.route("/asistencia")
def asistencia():
    return render_template("asistencia.html")