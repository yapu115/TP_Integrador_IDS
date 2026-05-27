from flask import Blueprint, render_template

notas_bp = Blueprint("notas", __name__)


@notas_bp.route("/notas", methods=["GET"])
def mostrar_notas():
    return render_template("notas.html")
