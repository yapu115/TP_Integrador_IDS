from flask import Blueprint, render_template, request, redirect, url_for, session

from services.api_client import get_json
from utils.auth import login_required

cursos_bp = Blueprint("cursos", __name__)

@cursos_bp.route("/seleccionar-curso", methods=["GET", "POST"])
@login_required
def seleccionar_curso():
    token = session.get("token")
    
    if request.method == "POST":
        curso_id = request.form.get("curso_id")
        curso_nombre = request.form.get("curso_nombre")
        if curso_id:
            session["curso_id"] = curso_id
            if curso_nombre:
                session["curso_nombre"] = curso_nombre
            return redirect(url_for("home.home"))

    status, data = get_json("/cursos", token=token)
    
    if status in (401, 403):
        session.clear()
        return redirect(url_for("auth.login"))
        
    cursos = data if status == 200 else []
    
    return render_template("cursos.html", cursos=cursos)


@cursos_bp.route("/crear-curso", methods=["GET", "POST"])
@login_required
def crear_curso():
    token = session.get("token")

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        fecha_inicio = request.form.get("fecha_inicio")
        fecha_fin = request.form.get("fecha_fin")

        if not nombre:
            return render_template("crear_curso.html", error="El nombre del curso es obligatorio.")

        body = {
            "nombre": nombre,
            "descripcion": descripcion if descripcion else None,
            "fecha_inicio": fecha_inicio if fecha_inicio else None,
            "fecha_fin": fecha_fin if fecha_fin else None
        }

        from services.api_client import post_json
        status, data = post_json("/cursos", body, token=token)

        if status == 201:
            session["curso_id"] = str(data.get("id"))
            session["curso_nombre"] = nombre
            return redirect(url_for("home.home"))
        else:
            errores = data.get("errors", [])
            msg = errores[0].get("message", "Error al crear curso") if errores else "Error desconocido"
            return render_template("crear_curso.html", error=msg)

    return render_template("crear_curso.html")
