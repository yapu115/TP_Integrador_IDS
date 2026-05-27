from flask import Blueprint, render_template

evaluaciones_bp = Blueprint('evaluaciones', __name__)


@evaluaciones_bp.route("/evaluaciones",methods=["GET"])
def mostrar_evaluaciones():
    return render_template('evaluaciones.html')