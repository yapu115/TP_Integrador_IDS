from flask import Blueprint, render_template, request
from urllib.parse import quote

from services.api_client import get_json


portal_alumno_bp = Blueprint("portal_alumno", __name__)


def primer_mensaje_error(data):
    errores = data.get("errors", []) if isinstance(data, dict) else []
    if errores:
        return errores[0].get("message", "Ocurrio un error.")
    return "Ocurrio un error."


@portal_alumno_bp.route("/alumno", methods=["GET", "POST"])
def portal_alumno():
    padron = ""
    datos = None
    error = None

    if request.method == "POST":
        padron = request.form.get("padron", "").strip()
        if not padron:
            error = "Ingrese su numero de padron."
        else:
            status, data = get_json(f"/alumnos/portal?padron={quote(padron)}")
            if status == 200:
                datos = data
            else:
                error = primer_mensaje_error(data)

    return render_template(
        "portal_alumno.html",
        padron=padron,
        datos=datos,
        error=error,
    )
