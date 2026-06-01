from flask import Blueprint, render_template, request, session, jsonify
from utils.auth import login_required

grupos_bp = Blueprint('grupos', __name__)

@grupos_bp.route("/grupos", methods=["GET", "POST"])
@login_required
def grupos():
    #Guardar grupos en un diccionario y pasarlos al template
    if request.method == "POST":
        #Si el metodo es post, se deben pasar los alumnos del grupo seleccionado
        return render_template("grupos.html")
    return render_template("grupos.html")
