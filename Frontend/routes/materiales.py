from flask import Blueprint, render_template, request, session, redirect, url_for
from utils.auth import login_required
from services.api_client import get_json, post_json

materiales_bp = Blueprint("materiales", __name__)

@materiales_bp.route("/materiales", methods=["GET", "POST"])
@login_required
def materiales():
    token = session.get("token")
    curso_id = session.get("curso_id")
    
    error = None
    exito = None

    if request.method == "POST":
        titulo = request.form.get("titulo")
        url_archivo = request.form.get("url_archivo")
        
        if not titulo or not url_archivo:
            error = "Todos los campos son obligatorios."
        else:
            status, data = post_json(f"/materiales?curso_id={curso_id}", {
                "titulo": titulo,
                "url_archivo": url_archivo
            }, token=token)
            
            if status == 201:
                exito = "Material agregado correctamente."
            else:
                errores = data.get("errors", [])
                error = errores[0].get("message", "Error al guardar el material.") if errores else "Error desconocido."

    # Obtener lista de materiales
    status, data = get_json(f"/materiales?curso_id={curso_id}", token=token)
    lista_materiales = data if status == 200 else []

    return render_template("materiales.html", materiales=lista_materiales, error=error, exito=exito)
